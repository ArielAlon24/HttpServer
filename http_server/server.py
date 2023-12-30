from .handlers import LoggingHandler, ClientHandler
from .enums import Method, ContentType, StatusCode
from .models import Resource, Route
from .utils.file import FileUtils
from .types import CreatorType, Creator

from typing import Callable, List, Dict
from concurrent.futures import ThreadPoolExecutor
import socket

logger = LoggingHandler.create_logger(__name__)


class Server:
    def __init__(
        self,
        ip: str = "0.0.0.0",
        port: int = 80,
        max_clients: int = 10,
    ) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        self.socket.listen(max_clients)

        self.routes: Dict[Route, Resource] = {}
        self.error_routes: Dict[StatusCode, Resource] = {}

        logger.debug(
            f"Initiated {self.__class__.__name__} on ({ip}, {port}) with {max_clients} max clients."
        )

    def route(
        self,
        method: Method = Method.GET,
        path: str = "/",
        content_type: ContentType = ContentType.HTML,
        success_status: StatusCode = StatusCode.OK,
    ) -> Callable[[CreatorType], CreatorType]:
        def decorator(function: CreatorType) -> CreatorType:
            self.add_route(
                function=function,
                method=method,
                path=path,
                content_type=content_type,
                success_status=success_status,
            )

            return function

        return decorator

    def error(
        self,
        status: StatusCode,
        content_type: ContentType = ContentType.HTML,
    ) -> Callable[[CreatorType], CreatorType]:
        def decorator(function: CreatorType) -> CreatorType:
            self.add_error_routes(
                statuses=[status], function=function, content_type=content_type
            )

            return function

        return decorator

    def add_error_routes(
        self,
        statuses: List[StatusCode],
        function: Creator,
        content_type: ContentType,
    ):
        for status in statuses:
            if status == StatusCode.OK:
                logger.error(
                    f"Cannot add an error route for {StatusCode.OK} status code."
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
        function: Creator,
        method: Method = Method.GET,
        path: str = "/",
        content_type: ContentType = ContentType.HTML,
        success_status: StatusCode = StatusCode.OK,
        _debug: bool = True,
    ) -> None:
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
        success_status: StatusCode = StatusCode.OK,
    ) -> None:
        def function():
            return FileUtils.read(path=file_path)

        function.__name__ = FileUtils.read.__name__
        self.add_route(
            function=function,
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
        try:
            self._run(max_workers=max_workers)
        except KeyboardInterrupt:
            self.close()

    def close(self) -> None:
        logger.debug("Closed server.")
        self.socket.close()
