from typing import Self, Callable, Tuple, Dict
from handlers.logging_handler import LoggingHandler
from handlers.client_handler import ClientHandler
from enums.methods import Method
from enums.content_types import ContentType
from models.resource import Resource
import socket
from logging import Logger
from concurrent.futures import ThreadPoolExecutor

logger: Logger = LoggingHandler.create_logger(__name__)


class HttpServer:
    def __init__(
        self, ip: str = "0.0.0.0", port: int = 80, max_clients: int = 10
    ) -> Self:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        self.socket.listen(max_clients)

        self.routes: Dict[str, Resource] = {}

        logger.debug(
            f"Initiated {self.__class__.__name__} on ({ip}, {port}) with {max_clients} max clients."
        )

    def route(
        self,
        path: str = "/",
        method: Method = Method.GET,
        content_type: ContentType = ContentType.HTML,
    ) -> Callable[Tuple, str]:
        def wrapper(function: Callable[Tuple, str]) -> Callable[Tuple, str]:
            self.routes[path] = Resource(function=function, content_type=content_type)
            logger.debug(
                f"Added route '{method.name} {path}' with function '{function.__name__}' to routes."
            )

        return wrapper

    def _run(self, max_workers: int) -> None:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                socket, address = self.socket.accept()
                logger.debug(f"Accepted connection from {address}.")
                client_handler = ClientHandler(socket=socket, address=address)

                executor.submit(client_handler.handle, self.routes)

    def run(self, max_workers: int = 5) -> None:
        try:
            self._run(max_workers=max_workers)
        except KeyboardInterrupt:
            self.close()

    def close(self) -> None:
        logger.debug("Closed server.")
        self.socket.close()
