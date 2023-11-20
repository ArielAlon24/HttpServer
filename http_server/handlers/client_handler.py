"""
Name: Ariel Alon
Description:
    This module defines the 'ClientHandler' class for handling
    each connected client.
"""

from http_server.models.request import Request
from .logging_handler import LoggingHandler
from ..models import status_code
from ..models.http_error import HttpError
from ..models.response import Response
from ..models.resource import Resource
from ..models.route import Route
from ..models.status_code import StatusCode
from ..utils import http

from typing import Tuple, Dict, Any
import socket
from logging import Logger

# the global logger of this module
logger: Logger = LoggingHandler.create_logger(__name__)


class ClientHandler:
    """
    A class for handling a client request.

    Attributes:
        socket (socket.socket): The client's socket.
        address (Tuple[str, int]): The address of the client (IP, port).
        routes: (Dict[Route, Resource]): The server's routes.
        timeout: (float): Request timeout time (in seconds).
    """

    def __init__(
        self,
        socket: socket.socket,
        address: Tuple[str, int],
        routes: Dict[Route, Resource],
        error_routes: Dict[StatusCode, Resource],
        timeout: float = 0.5,
    ) -> None:
        """
        Initialize a ClientHandler.

        Parameters:
            socket (socket.socket): The client's socket.
            address (Tuple[str, int]): The address of the client (IP, port).
            routes: (Dict[Route, Resource]): The server's routes.
            timeout: (float): Request timeout time (in seconds).
        """
        self.socket = socket
        self.address = address
        self.routes = routes
        self.error_routes = error_routes

        self.socket.settimeout(timeout)
        logger.debug(f"Initiated {self.__class__.__name__} on {self.address}.")

    def handle(self) -> None:
        """
        Handling a client request, and sending back correct response.
        """
        try:
            self._handle()
        except Exception as e:
            logger.error(repr(e))
        finally:
            self._close()

    def _close(self) -> None:
        """
        Closing the connection with the client gracefully.
        """
        self.socket.close()
        logger.debug(f"Closed connection with {self.address}.")

    def _handle(self) -> None:
        """
        The private handle function, generates the response and sends it
        to the client.
        """
        response = self._generate_response()

        self.socket.send(response.to_bytes())
        logger.debug(f"Sent response for {self.address} request.")

    def _generate_response(self) -> Response:
        """
        Generating the resposne to the request sent from the client.

        Returns:
            response (Response): Generated response.
        """
        try:
            raw_request = self._receive_raw_request()
            logger.debug(f"Received {self.address} request.")

            request = self._parse_request(raw_request)
            logger.debug(f"Parsed {self.address} request: {request.header()}")

            resource = self._find_resource(request)
            logger.debug(f"Found {self.address} requested resource.")

            content = self._execute_resource(resource=resource, request=request)
            logger.debug(
                f"{self.address} request matched function ("
                + f"{resource.function.__name__}) arguments."
            )

            response = self._content_to_response(resource=resource, content=content)
            logger.debug(f"Response for {self.address} created.")
        except Exception as error:
            logger.warning(
                f"Couldn't create response for {self.address}, trying to create error response."
            )
            return self._generate_error_response(error=error)
        return response

    def _generate_error_response(
        self, error: Exception, max_tries: int = 3
    ) -> Response:
        """
        Generating an error resposne to the error prone request sent from the client.

        Parameters:
            error (Exception): The error that triggered this response.
            max_tries (int): If the creation fails, how many retries are allowed.

        Returns:
            response (Response): Generated response.
        """
        if isinstance(error, HttpError):
            status = error.status_code
        else:
            status = status_code.INTERNAL_SERVER_ERROR

        if status not in self.error_routes.keys():
            return Response.from_error(status_code=status, error=error)
        resource = self.error_routes[status]
        logger.debug(f"Found '{status}' error resource for {self.address}.")

        try:
            content = resource.function()
            logger.debug(f"{self.address} {status} error content created.")
            response = self._content_to_response(resource=resource, content=content)
            logger.debug(f"{self.address} {status} error response generated.")
        except (HttpError, Exception) as error:
            logger.error(
                f"Couldn't create {status} error for {self.address}"
                + f" ({max_tries} tries left): {repr(error)}"
            )
            if max_tries <= 1:
                return Response.from_error(error=error)
            response = self._generate_error_response(
                error=error, max_tries=max_tries - 1
            )
        return response

    def _receive_raw_request(self, size: int = 4096) -> str:
        """
        A private method for receiving the request from the client.

        Parameters:
            size (int): The size in bytes of the received data.

        Returns:
            received data (str): The request of the client as a string.
        """
        try:
            raw_request = self.socket.recv(size).decode("utf-8")
        except socket.error as error:
            raise HttpError(
                message=f"Could not receive data from client at {self.address}.",
                status_code=status_code.BAD_REQUEST,
            )
        if not raw_request:
            raise HttpError(
                message=f"No data received from client at {self.address}.",
                status_code=status_code.BAD_REQUEST,
            )

        return raw_request

    def _parse_request(self, raw_request: str) -> Request:
        """
        A private method for parsing a raw request.

        Parameters:
            raw_request (str): Raw request string.

        Returns:
            request (Request): Parsed Reuqest.
        """
        try:
            request = http.parse(raw_request)
        except ValueError as error:
            raise HttpError(
                message=f"Could not parse {self.address} request.",
                status_code=status_code.BAD_REQUEST,
            )
        return request

    def _find_resource(self, request: Request) -> Resource:
        """
        A private method for finding a resource based on a request.

        Parmeters:
            request (Request): Request instance.

        Returns:
            resource (Resource): Request's resource.
        """
        try:
            resource = self.routes[Route(method=request.method, path=request.path)]
        except KeyError as error:
            raise HttpError(
                message=f"Could not find {self.address} request's resource.",
                status_code=status_code.NOT_FOUND,
            )
        return resource

    def _execute_resource(
        self, resource: Resource, request: Request
    ) -> str | bytes | None:
        """
        A private method for executing a resource.

        Parmaeters:
            resource (Resource): resource to execute.
            request (Request): Resource's Request.

        Returns:
            content (str | bytes | None): Executed resource content.
        """
        kwargs: Dict[str, Any] = request.parameters
        function_arguments = resource.function.__annotations__
        if request.PAYLOAD_KEY in function_arguments:
            kwargs[request.PAYLOAD_KEY] = request.payload
        if request.HEADERS_KEY in function_arguments:
            kwargs[request.HEADERS_KEY] = request.headers
        try:
            content = resource.function(**kwargs)
        except TypeError as error:
            raise HttpError(
                message=f"Could not execute {self.address} request's resource.",
                status_code=status_code.BAD_REQUEST,
            )
        return content

    def _content_to_response(
        self, resource: Resource, content: str | bytes | None
    ) -> Response:
        """
        A private method to generate a respone instance from
        a resource and it's content.

        Parameters:
            resource (Resource): Content's resource.
            content (str | bytes | None): content.

        Returns:
            responsne (Response): The generated resposne.
        """
        if not content:
            return Response(
                status_code=status_code.OK,
                content_type=resource.content_type,
            )
        elif isinstance(content, str):
            return Response(
                status_code=status_code.OK,
                content=content.encode(),
                content_type=resource.content_type,
            )
        elif isinstance(content, bytes):
            return Response(
                status_code=status_code.OK,
                content=content,
                content_type=resource.content_type,
            )
        else:
            raise HttpError(
                message="{self.address} resource function does not return 'str', 'bytes' or 'None'.",
                status_code=status_code.INTERNAL_SERVER_ERROR,
            )
