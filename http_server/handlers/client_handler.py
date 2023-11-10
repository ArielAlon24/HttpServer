"""
Name: Ariel Alon
Description:
    This module defines the 'ClientHandler' class for handling
    each connected client.
"""

from .logging_handler import LoggingHandler
from ..models.status_codes import StatusCode
from ..models.response import Response
from ..models.resource import Resource
from ..models.route import Route
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

    def _receive_request(self, size: int = 4096) -> str:
        """
        A private function for receiving the request from the client.

        Parameters:
            size (int): The size in bytes of the received data.

        Returns:
            received data (str): The request of the client as a string.
        """
        try:
            data = self.socket.recv(size).decode("utf-8")
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
        """
        Private generate response.

        Returns:
            response (Response): The response generated.
        """

        # Receiving raw request
        try:
            raw_request = self._receive_request()
        except ConnectionError as error:
            logger.warning(repr(error))
            return Response.create_error(
                status_code=StatusCode.bad_request(), error=error
            )
        logger.debug(f"Received {self.address} request.")

        # Parsing request string
        try:
            request = http.parse(raw_request)
        except ValueError as error:
            logger.warning(repr(error))
            return Response.create_error(
                status_code=StatusCode.bad_request(), error=error
            )
        logger.debug(f"Parsed {self.address} request: {request.header()}")

        # Finding correct resource
        try:
            resource = self.routes[
                Route(method=request.method, path=request.path)
            ]
        except KeyError as error:
            logger.warning(repr(error))
            return Response.create_error(
                status_code=StatusCode.not_found(), error=error
            )
        logger.debug(f"Found {self.address} requested resource.")

        # Injecting correct arguments and running the creating function.
        try:
            kwargs: Dict[str, Any] = request.parameters
            function_arguments = resource.function.__annotations__
            if request.PAYLOAD_KEY in function_arguments:
                kwargs[request.PAYLOAD_KEY] = request.payload
            if request.HEADERS_KEY in function_arguments:
                kwargs[request.HEADERS_KEY] = request.headers

            content = resource.function(**kwargs)
        except TypeError as error:
            logger.warning(repr(error))
            return Response.create_error(
                status_code=StatusCode.bad_request(), error=error
            )
        logger.debug(
            f"{self.address} request matched function (\
            {resource.function.__name__}) arguments."
        )

        # Encoding if needed.
        try:
            if not content:
                return Response(
                    status_code=StatusCode.ok(),
                    content_type=resource.content_type,
                )
            elif isinstance(content, str):
                return Response(
                    status_code=StatusCode.ok(),
                    content=content.encode(),
                    content_type=resource.content_type,
                )
            elif isinstance(content, bytes):
                return Response(
                    status_code=StatusCode.ok(),
                    content=content,
                    content_type=resource.content_type,
                )
            else:
                raise ValueError(
                    "Resource functions must return 'str', 'bytes' or 'None'."
                )
        except ValueError as error:
            logger.warning(repr(error))
            return Response.create_error(
                status_code=StatusCode.internal_server_error(), error=error
            )
