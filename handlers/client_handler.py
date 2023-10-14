from typing import Self, Tuple, Dict, Callable
import socket
from logging import Logger

from models.response import Response
from handlers.logging_handler import LoggingHandler
from utils import parsing
from enums.status_codes import OK, BAD_REQUEST, NOT_FOUND, INTERNAL_SERVER_ERROR


logger: Logger = LoggingHandler.create_logger(__name__)


class ClientHandler:
    def __init__(
        self,
        socket: socket.socket,
        address: Tuple[str, int],
        time_out: int = 0.5,
    ) -> Self:
        self.socket = socket
        self.address = address

        logger.debug(f"Initiated {self.__class__.__name__} on {self.address}.")

    def _receive_request(self) -> str:
        try:
            data = self.socket.recv(1024).decode("utf-8")
        except socket.error:
            raise ConnectionError(
                f"Could not receive data from client at {self.address}."
            )
        if not data:
            raise ConnectionError(
                f"Could not receive data from client at {self.address}."
            )
        return data

    def _generate_response(self, routes: Dict[str, Callable[Tuple, str]]) -> Response:
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
            resource = routes[request.path]
        except KeyError as error:
            logger.warning(repr(error))
            return Response(status_code=NOT_FOUND, content=repr(error).encode())
        logger.debug(f"Found {self.address} requested resource.")

        try:
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

    def handle(self, routes: Dict[str, Callable[Tuple, str]]) -> None:
        response = self._generate_response(routes=routes)

        self.socket.send(response.to_bytes())
        logger.debug(f"Sent response for {self.address} request.")

        self.socket.close()
        logger.debug(f"Closed connection with {self.address}.")
