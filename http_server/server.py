"""
Name: Ariel Alon
Description:
    This module defines the 'Server' class and all related methods.
"""

from .handlers.logging_handler import LoggingHandler
from .handlers.client_handler import ClientHandler
from .enums.methods import Method
from .enums.content_types import ContentType
from .models.resource import Resource
from .models.route import Route
from .models.status_code import StatusCode
from .models import status_code
from .utils import file

from typing import Callable, Dict, List
from logging import Logger
from concurrent.futures import ThreadPoolExecutor
import socket

# logger for the 'server' module
logger: Logger = LoggingHandler.create_logger(__name__)


class Server:
    """
    A class that represents an HTTP server.

    Attributes:
        socket (socket.scoket): Server's TCP socket.
        ip (str): The Server's IP.
        port (int): The Server's port.
        max_clients (int): Total number of connected clients simultaneously.
        routes (Dict[Route, Resource]): Server's routes.
        error_routes (Dict[StatusCode, Resource]): Server's error routes.
    """

    def __init__(
        self,
        ip: str = "0.0.0.0",
        port: int = 80,
        max_clients: int = 10,
    ) -> None:
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
        self.error_routes: Dict[StatusCode, Resource] = {}

        logger.debug(
            f"Initiated {self.__class__.__name__} on ({ip}, {port}) "
            + f"with {max_clients} max clients."
        )

    def route(
        self,
        method: Method = Method.GET,
        path: str = "/",
        content_type: ContentType = ContentType.HTML,
        success_status: StatusCode = status_code.OK,
    ) -> Callable[..., None]:
        """
        A decorator for adding a route to the to the server.

        Parameters:
            method (Method): The method type of the request.
            path (str): A string path for the route to be added.
            content_type (ContentType):
                The content type of the resource of the route.

        Returns:
            Callable[..., None]: The wrapper.
        """

        def wrapper(function: Callable[..., str | bytes | None]) -> None:
            """
            The inner function of the decorator.

            Parameters:
                function (Callable[..., str | bytes | None]): The decorated function.
            """
            self.add_route(
                function=function,
                method=method,
                path=path,
                content_type=content_type,
                success_status=success_status,
            )

        return wrapper

    def error(
        self,
        status: StatusCode,
        content_type: ContentType = ContentType.HTML,
    ) -> Callable[..., None]:
        """
        A decorator for adding an error route to the to the server.

        Parameters:
            status (StatusCode): Error status code.
            content_type (ContentType):
                The content type of the resource of the route.

        Returns:
            Callable[..., None]: The wrapper.
        """

        def wrapper(function: Callable[..., str | bytes | None]) -> None:
            """
            The inner function of the decorator.

            Parameters:
                function (Callable[..., str | bytes | None]): The decorated function.
            """
            self.add_error_routes(
                statuses=[status], function=function, content_type=content_type
            )

        return wrapper

    def add_error_routes(
        self,
        statuses: List[StatusCode],
        function: Callable[..., str | bytes | None],
        content_type: ContentType,
    ):
        """
        Add a error routes to the to the server.

        Parameters:
            statuses (List[StatusCode]):
                All errors that route this route.
            function (Callable[..., str | bytes | None]):
                Resource creating function.
            content_type (ContentType):
                The content type of the resource of the route.
        """
        for status in statuses:
            if status == status_code.OK:
                logger.error(
                    f"Cannot add an error route for {status_code.OK} status code."
                )
                continue
            self.error_routes[status] = Resource(
                function=function,
                content_type=content_type,
                success_status=status,
            )
            logger.debug(
                f"Added error route '{status}' to function "
                + f"'{function.__name__}' with {content_type.name} content type."
            )

    def add_route(
        self,
        function: Callable[..., str | bytes | None],
        method: Method = Method.GET,
        path: str = "/",
        content_type: ContentType = ContentType.HTML,
        success_status: StatusCode = status_code.OK,
        _debug: bool = True,
    ) -> None:
        """
        Add a route to the to the server.

        Parameters:
            function (Callable[..., str | bytes | None]):
                Resource creating function.
            method (Method): The method type of the request.
            path (str): A string path for the route to be added.
            content_type (ContentType):
                The content type of the resource of the route.
            _debug (bool): Is route addition logged.
        """
        self.routes[Route(method=method, path=path)] = Resource(
            function=function,
            content_type=content_type,
            success_status=success_status,
        )

        if _debug:
            logger.debug(
                f"Added route '{method.name} {path}' to function "
                + f"'{function.__name__}' with {content_type.name} content type."
            )

    def add_file_route(
        self,
        file_path: str,
        method: Method = Method.GET,
        path: str = "/",
        content_type: ContentType = ContentType.HTML,
        success_status: StatusCode = status_code.OK,
    ) -> None:
        """
        Add a file route to the to the server.

        Parameters:
            file_path (str): Resource file.
            method (Method): The method type of the request.
            path (str): A string path for the route to be added.
            content_type (ContentType):
                The content type of the resource of the route.
        """
        self.add_route(
            function=lambda: file.read(path=file_path),
            method=method,
            path=path,
            content_type=content_type,
            success_status=success_status,
            _debug=False,
        )

        logger.debug(
            f"Added route '{method.name} {path}' to '{file_path}' "
            + f"file contents with {content_type.name} content type."
        )

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
                    socket=socket,
                    address=address,
                    routes=self.routes,
                    error_routes=self.error_routes,
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
