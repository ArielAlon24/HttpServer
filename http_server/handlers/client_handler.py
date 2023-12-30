from http_server.models.request import Request
from .logging_handler import LoggingHandler
from ..models import HttpError, Response, Resource, Route, Redirect, Cookie
from ..enums.status_codes import StatusCode
from ..utils.http import HttpParser
from ..types import Content

from typing import Tuple, Dict, Set, Any
import socket

logger = LoggingHandler.create_logger(__name__)


class ClientHandler:
    CHUNK_SIZE = 2048

    def __init__(
        self,
        socket: socket.socket,
        address: Tuple[str, int],
        routes: Dict[Route, Resource],
        error_routes: Dict[StatusCode, Resource],
        timeout: float = 0.5,
    ) -> None:
        self.socket = socket
        self.address = address
        self.routes = routes
        self.error_routes = error_routes

        self.socket.settimeout(timeout)
        logger.debug(f"Initiated {self.__class__.__name__} on {self.address}.")

    def handle(self) -> None:
        try:
            self._handle()
        except Exception as e:
            logger.error(repr(e))
        finally:
            self._close()

    def _close(self) -> None:
        self.socket.close()
        logger.debug(f"Closed connection with {self.address}.")

    def _handle(self) -> None:
        response = self._generate_response()

        if len(response.to_bytes()) <= self.CHUNK_SIZE:
            self._send(response)
        else:
            self._send_chunks(response)

    def _send(self, response: Response) -> None:
        self.socket.send(response.to_bytes())
        logger.debug(f"Sent full response for {self.address} request.")

    def _send_chunks(self, response: Response) -> None:
        response_bytes = response.to_bytes()
        count = 0
        for i in range(0, len(response_bytes), self.CHUNK_SIZE):
            chunk = response_bytes[i : i + self.CHUNK_SIZE]
            self.socket.send(chunk)
            count += 1

        logger.debug(
            f"Completed sending all response chunks "
            + f"({count}) for {self.address} request."
        )

    def _generate_response(self) -> Response:
        try:
            raw_request = self._receive_raw_request()
            logger.debug(f"Received {self.address} request.")

            request = self._parse_request(raw_request)
            logger.debug(f"Parsed {self.address} request: {request.header()}")

            resource = self._find_resource(request)
            logger.debug(f"Found {self.address} requested resource.")

            kwargs = self._load_kwargs(resource=resource, request=request)
            logger.debug(f"Loaded {self.address} kwargs.")

            content, headers, cookies = self._execute_resource(
                resource=resource, kwargs=kwargs
            )

            logger.debug(
                f"{self.address} request matched function ("
                + f"{resource.function.__name__}) arguments."
            )

            response = self._content_to_response(
                resource=resource,
                content=content,
                headers=headers,
                cookies=cookies,
            )
            logger.debug(f"Response for {self.address} created.")
        except Exception as error:
            logger.warning(
                f"Couldn't create response for {self.address}, "
                + "trying to create error response."
            )
            return self._generate_error_response(error=error)
        return response

    def _generate_error_response(
        self, error: Exception, max_tries: int = 3
    ) -> Response:
        if isinstance(error, HttpError):
            status = error.status_code
        else:
            status = StatusCode.INTERNAL_SERVER_ERROR

        if status not in self.error_routes.keys():
            return Response.from_error(status_code=status, error=error)
        resource = self.error_routes[status]
        logger.debug(f"Found '{repr(status.value)}' error resource for {self.address}.")

        try:
            headers: Dict[str, str] = {}
            cookies: Set[Cookie] = set()
            content, headers, cookies = self._execute_resource(resource)
            logger.debug(f"{self.address} {status} error content created.")
            response = self._content_to_response(
                resource=resource,
                content=content,
                headers=headers,
                cookies=cookies,
            )
            logger.debug(f"{self.address} {status} error response generated.")
        except (HttpError, Exception) as error:
            logger.warning(
                f"Could not create {status} resource for {self.address}"
                + f" ({max_tries} tries left): {repr(error)}"
            )
            if max_tries <= 1:
                logger.debug(
                    f"Creating default error for: {self.address}. "
                    + f"Reason: {repr(error)}"
                )
                return Response.from_error(error=error)
            response = self._generate_error_response(
                error=error, max_tries=max_tries - 1
            )
        return response

    def _receive_raw_request(self, size: int = 4096) -> str:
        try:
            raw_request = self.socket.recv(size).decode("utf-8")
        except socket.error:
            raise HttpError(
                message=f"Could not receive data from client at {self.address}.",
                status_code=StatusCode.BAD_REQUEST,
            )
        if not raw_request:
            raise HttpError(
                message=f"No data received from client at {self.address}.",
                status_code=StatusCode.BAD_REQUEST,
            )

        return raw_request

    def _parse_request(self, raw_request: str) -> Request:
        try:
            request = HttpParser.parse(raw_request)
        except ValueError:
            raise HttpError(
                message=f"Could not parse {self.address} request.",
                status_code=StatusCode.BAD_REQUEST,
            )
        return request

    def _find_resource(self, request: Request) -> Resource:
        try:
            resource = self.routes[Route(method=request.method, path=request.path)]
        except KeyError:
            raise HttpError(
                message=f"Could not find {self.address} request's resource.",
                status_code=StatusCode.NOT_FOUND,
            )
        return resource

    def _load_kwargs(self, resource: Resource, request: Request) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = request.parameters
        function_arguments = resource.function.__annotations__
        if Request.PAYLOAD_KEY in function_arguments:
            kwargs[Request.PAYLOAD_KEY] = request.payload
        if Request.HEADERS_KEY in function_arguments:
            kwargs[Request.HEADERS_KEY] = request.headers
        if Request.COOKIES_KEY in function_arguments:
            kwargs[Request.COOKIES_KEY] = request.cookies
        return kwargs

    def _execute_resource(
        self, resource: Resource, kwargs: Dict[str, Any] | None = None
    ) -> Tuple[Content, Dict[str, str], Set[Cookie]]:
        kwargs = kwargs if kwargs else {}
        try:
            content = resource.function(**kwargs)
        except TypeError as error:
            raise HttpError(
                message=f"Could not execute {self.address} request's resource.",
                status_code=StatusCode.BAD_REQUEST,
            )

        cookies: Set[Cookie] = getattr(resource.function, Response.COOKIES_KEY, set())
        headers: Dict[str, str] = getattr(resource.function, Response.HEADERS_KEY, {})
        return content, headers, cookies

    def _content_to_response(
        self,
        resource: Resource,
        content: Content,
        headers: Dict[str, str],
        cookies: Set[Cookie],
    ) -> Response:
        if content is None:
            return Response(
                status_code=resource.success_status,
                content_type=resource.content_type,
                headers=headers,
                cookies=cookies,
            )
        elif isinstance(content, Redirect):
            return Response.from_redirect(content)
        elif isinstance(content, str):
            return Response(
                status_code=resource.success_status,
                content=content.encode(),
                content_type=resource.content_type,
                headers=headers,
                cookies=cookies,
            )
        elif isinstance(content, bytes):
            return Response(
                status_code=resource.success_status,
                content=content,
                content_type=resource.content_type,
                headers=headers,
                cookies=cookies,
            )
        else:
            raise HttpError(
                message=f"{self.address} resource function does not "
                + f"return {repr(str)}, {repr(bytes)} or {repr(None)}.",
                status_code=StatusCode.INTERNAL_SERVER_ERROR,
            )
