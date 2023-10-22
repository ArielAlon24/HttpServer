from typing import Self, Tuple, Dict
import socket
from logging import Logger

from .logging_handler import LoggingHandler
from ..enums.status_codes import OK, BAD_REQUEST, NOT_FOUND, INTERNAL_SERVER_ERROR
from ..models.response import Response
from ..models.resource import Resource
from ..models.route import Route
from ..utils import parsing

logger: Logger = LoggingHandler.create_logger(__name__)


class ClientHandler:
    def __init__(
        self,
        socket: socket.socket,
        address: Tuple[str, int],
        routes: Dict[Route, Resource],
        timeout: float = 0.5,
    ) -> Self:
        self.socket = socket
        self.address = address
        self.routes = routes

        self.socket.settimeout(timeout)
        logger.debug(f"Initiated {self.__class__.__name__} on {self.address}.")

    def handle(self) -> None:
        try:
            self._handle()
        except Exception as e:
            logger.error(repr(e))
        finally:
            self.close()

    def _close(self) -> None:
        self.socket.close()
        logger.debug(f"Closed connection with {self.address}.")

    def _handle(self) -> None:
        response = self._generate_response()

        self.socket.send(response.to_bytes())
        logger.debug(f"Sent response for {self.address} request.")

    def _receive_request(self) -> str:
        try:
            data = self.socket.recv(4096).decode("utf-8")
        except socket.error:
            raise ConnectionError(
                f"Could not receive data from client at {self.address}."
            )
        if not data:
            raise ConnectionError(
                f"Could not receive data from client at {self.address}."
            )
        return data

    def _generate_response(self) -> Response:
        try:
            raw_request = self._receive_request()
        except ConnectionError as error:
            logger.warning(repr(error))
            return Response(status_code=BAD_REQUEST, content=repr(error).encode())
        logger.debug(f"Received {self.address} request.")

        try:
            request = parsing.parse(raw_request)
        except ValueError as error:
            logger.warning(repr(error))
            return Response(status_code=BAD_REQUEST, content=repr(error).encode())
        logger.debug(f"Parsed {self.address} request: {request.header()}")

        try:
            resource = self.routes[Route(method=request.method, path=request.path)]
        except KeyError as error:
            logger.warning(repr(error))
            return Response(status_code=NOT_FOUND, content=repr(error).encode())
        logger.debug(f"Found {self.address} requested resource.")

        try:
            if resource.include_payload:
                content = resource.function(
                    **request.parameters, payload=request.payload
                )
            else:
                content = resource.function(**request.parameters)
        except TypeError as error:
            logger.warning(repr(error))
            return Response(status_code=BAD_REQUEST, content=repr(error).encode())
        logger.debug(f"{self.address} request parameters matched.")

        try:
            if isinstance(content, str):
                return Response(
                    status_code=OK,
                    content=content.encode(),
                    content_type=resource.content_type,
                )
            elif isinstance(content, bytes):
                return Response(
                    status_code=OK, content=content, content_type=resource.content_type
                )
            else:
                raise ValueError("Resource functions must return 'str' or 'bytes'.")
        except ValueError as error:
            logger.warning(repr(error))
            return Response(
                status_code=INTERNAL_SERVER_ERROR, content=repr(error).encode()
            )
