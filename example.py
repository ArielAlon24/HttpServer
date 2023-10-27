from http_server.server import Server
from http_server.enums.content_types import ContentType
from http_server.utils import file

from typing import Dict

app = Server()


@app.route(path="/favicon.ico", content_type=ContentType.IMAGE)
def favicon() -> bytes:
    return file.read(path="resources/favicon.ico")


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


if __name__ == "__main__":
    app.run()
