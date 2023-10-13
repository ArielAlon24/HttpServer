from typing import Self, Optional, Callable, Tuple, Dict
from handlers.logging_handler import LoggingHandler
from handlers.client_handler import ClientHandler
from enums.methods import Method
from enums.content_types import ContentType
from models.page import Page
import socket
from logging import Logger
import threading


class HttpServer:
    logger: Optional[Logger] = None
    IP: str = "0.0.0.0"
    PORT: int = 80

    def __init__(self, max_clients: int = 10) -> Self:
        if not HttpServer.logger:
            HttpServer.logger = LoggingHandler.create_logger(self.__class__.__name__)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen(max_clients)

        self.routes: Dict[str, Page] = {}

        HttpServer.logger.debug(
            f"Initiated {self.__class__.__name__} on ({self.IP}, {self.PORT}) with {max_clients} max clients."
        )

    def route(
        self,
        path: str = "/",
        method: Method = Method.GET,
        content_type: ContentType = ContentType.HTML,
    ) -> Callable[Tuple, str]:
        def wrapper(function: Callable[Tuple, str]) -> Callable[Tuple, str]:
            self.routes[path] = Page(function=function, content_type=content_type)
            HttpServer.logger.debug(
                f"Added route '{method.name} {path}' with function '{function.__name__}' to routes."
            )

        return wrapper

    def _run(self) -> None:
        while True:
            socket, address = self.socket.accept()
            HttpServer.logger.debug(f"Accepted connection from {address}.")
            client_handler = ClientHandler(socket=socket, address=address)

            client_thread = threading.Thread(
                target=client_handler.handle, args=(self.routes,)
            )

            client_thread.start()

    def run(self) -> None:
        try:
            self._run()
        except KeyboardInterrupt:
            self.close()

    def close(self) -> None:
        HttpServer.logger.debug("Closed server.")
        self.socket.close()
