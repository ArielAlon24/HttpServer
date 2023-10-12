from typing import Self, Tuple, Optional
import socket
from logging import Logger

from models.response import Response
from handlers.logging_handler import LoggingHandler
from utils import parsing_utils
from enums.status_codes import OK, BAD_REQUEST


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

    def handle(self) -> None:
        try:
            data = self._receive_request()

            _ = parsing_utils.parse(data)
            ClientHandler.logger.debug(f"Parsed {self.address} request.")
            response = Response(status_code=OK, content="<h1>Success!</h1>")
        except (ValueError, ConnectionError) as error:
            ClientHandler.logger.warning(
                f"Encountered an error while parsing {self.address} request."
            )
            response = Response(status_code=BAD_REQUEST, content=error)
        self.logger.debug(f"Created response for {self.address} request.")
        self.socket.send(str(response).encode())
        self.logger.debug(f"Sent response for {self.address} request.")
        self.socket.close()
        self.logger.debug(f"Closed connection with {self.address}.")

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
        ClientHandler.logger.debug(f"Received a request from {self.address}.")
        return data
