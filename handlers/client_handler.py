from typing import Self, Tuple, Optional, Dict, Callable
import socket
from logging import Logger

from models.response import Response
from handlers.logging_handler import LoggingHandler
from utils import parsing_utils
from enums.status_codes import OK, BAD_REQUEST, NOT_FOUND


class ClientHandler:
    logger: Optional[Logger] = None

    def __init__(
        self,
        socket: socket.socket,
        address: Tuple[str, int],
        time_out: int = 0.5,
    ) -> Self:
        if ClientHandler.logger is None:
            ClientHandler.logger = LoggingHandler.create_logger(self.__class__.__name__)
        self.socket = socket
        self.address = address

        ClientHandler.logger.debug(
            f"Initiated {self.__class__.__name__} on {self.address}."
        )

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
            ClientHandler.logger.warning(repr(error))
            return Response(status_code=BAD_REQUEST, content=repr(error))

        ClientHandler.logger.debug(f"Received {self.address} request.")

        try:
            request = parsing_utils.parse(raw_request)
        except ValueError as error:
            ClientHandler.logger.warning(repr(error))
            return Response(status_code=BAD_REQUEST, content=repr(error))

        ClientHandler.logger.debug(f"Parsed {self.address} request.")

        try:
            page = routes[request.path]
        except KeyError as error:
            ClientHandler.logger.warning(repr(error))
            return Response(status_code=NOT_FOUND, content=repr(error))
        ClientHandler.logger.debug(f"Found {self.address} requested page.")

        try:
            if request.parameters:
                content = page.function(**request.parameters)
            else:
                content = page.function()
        except TypeError as error:
            ClientHandler.logger.warning(repr(error))
            return Response(status_code=BAD_REQUEST, content=repr(error))

        ClientHandler.logger.debug(f"Created {self.address} requested page.")
        return Response(status_code=OK, content=content, content_type=page.content_type)

    def handle(self, routes: Dict[str, Callable[Tuple, str]]) -> None:
        response = self._generate_response(routes=routes)

        self.socket.send(response.to_bytes())
        self.logger.debug(f"Sent response for {self.address} request.")

        self.socket.close()
        self.logger.debug(f"Closed connection with {self.address}.")
