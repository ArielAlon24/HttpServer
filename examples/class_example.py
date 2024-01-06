from http_server import Server
from http_server.decorators import inject
from http_server.models import Cookie
from http_server.enums import ContentType
from http_server.utils import FileUtils

from typing import Dict


class App:
    def __init__(self) -> None:
        self.server = Server()
        self._setup()

    def serve(self) -> None:
        self.server.run()

    def _setup(self) -> None:
        self.server.add_file_route(
            file_path="resources/favicon.ico",
            content_type=ContentType.IMAGE,
            path="/favicon.ico",
        )
        self.server.add_file_route(
            file_path="resources/styles.css",
            content_type=ContentType.CSS,
            path="/styles.css",
        )

        self.server.add_route(function=self.index)
        self.server.add_route(function=self.set_cookie, path="/cookie")
        self.server.add_route(function=self.set_header, path="/header")
        self.server.add_route(function=self.add, path="/add")

    def index(
        self, payload: str, headers: Dict[str, str], cookies: Dict[str, Cookie]
    ) -> bytes:
        return FileUtils.template(
            path="resources/index.html",
            payload=payload,
            headers=repr(headers),
            cookies=repr(cookies),
        )

    @inject(cookies=True)
    def set_cookie(self) -> str:
        self.set_cookie.cookies.add(Cookie(name="test", value="123"))
        return "done"

    @inject(headers=True)
    def set_header(self) -> str:
        self.set_header.headers["test"] = "123"
        return "done"

    @staticmethod
    def add(a: str, b: str) -> str:
        result = int(a) + int(b)
        return f"<h1> Result = {result} </h1>"


if __name__ == "__main__":
    app = App()
    app.serve()
