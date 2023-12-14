from http_server.enums.status_code import StatusCode
from http_server.models.redirect import Redirect
from http_server.server import Server
from http_server.enums.content_types import ContentType
from http_server.utils import file

from typing import Dict

app = Server()

app.add_file_route(
    file_path="resources/favicon.ico",
    content_type=ContentType.IMAGE,
    path="/favicon.ico",
)


@app.route(path="/", content_type=ContentType.HTML)
def index(payload: str, headers: Dict[str, str]) -> bytes:
    return file.template(
        path="resources/index.html", payload=payload, headers=repr(headers)
    )


@app.route(path="/styles.css", content_type=ContentType.CSS)
def styles() -> bytes:
    return file.read(path="resources/styles.css")


@app.route(path="/add", content_type=ContentType.HTML)
def add(a: str, b: str) -> str:
    result = int(a) + int(b)
    return f"<h1> Result = {result} </h1>"


@app.route(path="/division", content_type=ContentType.HTML)
def division() -> str:
    division = 1 / 0
    return "Oh no!"


@app.error(status=StatusCode.NOT_FOUND, content_type=ContentType.HTML)
def not_found() -> str:
    return "<h1> Oops not found... </h1>"


@app.route(path="/redirect")
def redirect() -> Redirect:
    return Redirect(location="/")


@app.error(status=StatusCode.INTERNAL_SERVER_ERROR, content_type=ContentType.HTML)
def intenal_server_error() -> None:
    test = a + 2


if __name__ == "__main__":
    app.run()
