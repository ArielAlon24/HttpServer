"""
Name: Ariel Alon
Description: This module defines the 'Server' class and all related methods.
"""

from .handlers.logging_handler import LoggingHandler
from .handlers.client_handler import ClientHandler
from .enums.methods import Method
from .enums.content_types import ContentType
from .models.resource import Resource
from .models.route import Route

from typing import Self, Callable, Tuple, Dict
from logging import Logger
from concurrent.futures import ThreadPoolExecutor
import socket

# logger for the 'server' module
logger: Logger = LoggingHandler.create_logger(__name__)


class Server:
    """
    A class that represents an HTTP server.

    Attributes:
        ip (str): The Server's IP.
        port (int): The Server's port.
        max_clients (int): Total number of connected clients simultaneously.
    """

    def __init__(
        self,
        ip: str = "0.0.0.0",
        port: int = 80,
        max_clients: int = 10,
    ) -> Self:
        """
        Initialize an instance of a Server class at (IP, port).

        Parameters:
            ip (str): The IP of the server.
            port (int): The port of the server.
            max_clients (int):
                Total number of connected clients simultaneously.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        self.socket.listen(max_clients)

        self.routes: Dict[Route, Resource] = {}
        self.error_routes: Dict[Route, Resource] = {}

        logger.debug(
            f"Initiated {self.__class__.__name__} on ({ip}, {port})\
             with {max_clients} max clients."
        )

    def route(
        self,
        method: Method = Method.GET,
        path: str = "/",
        content_type: ContentType = ContentType.HTML,
    ) -> Callable[Tuple, str]:
        """
        A decorator for adding a route to the to the server.

        Parameters:
            method (Method): The method type of the request.
            path (str): A string path for the route to be added.
            content_type (ContentType):
                The content type of the resource of the route.

        Returns:
            Callable[Tuple, str]: a function that returns a str.
        """

        def wrapper(function: Callable[Tuple, str]) -> None:
            """
            The inner function of the decorator.

            Parameters:
                function (Callable[Tuple, str]): The decorated function.
            """
            self.routes[Route(method=method, path=path)] = Resource(
                function=function,
                content_type=content_type,
            )
            logger.debug(
                f"Added route '{method.name} {path}' to function\
                 '{function.__name__}' with {content_type.name} content type."
            )

        return wrapper

    def _run(self, max_workers: int) -> None:
        """
        The private run function for the server, starts a thread pool with
        max_workers for serving the server.

        Parameters:
            max_workers (int): Max workers for the ThreadPool.
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                try:
                    socket, address = self.socket.accept()
                except Exception as e:
                    logger.error(repr(e))
                    continue

                logger.debug(f"Accepted connection from {address}.")

                client_handler = ClientHandler(
                    socket=socket, address=address, routes=self.routes
                )

                executor.submit(client_handler.handle)

    def run(self, max_workers: int = 5) -> None:
        """
        The public run function for the server, runs the private run
        function. Catches any error raised up by the server.

        Parameters:
            max_workers (int): Max workers for the '_run' method ThreadPool.
        """
        try:
            self._run(max_workers=max_workers)
        except KeyboardInterrupt:
            self.close()

    def close(self) -> None:
        """
        Closing the server gracefully.
        """
        logger.debug("Closed server.")
        self.socket.close()
