from datetime import timedelta
from http_server import Server
from http_server.decorators import inject
from http_server.models import Redirect, Cookie, CacheControl
from http_server.enums import ContentType, StatusCode, HeaderType
from http_server.utils import FileUtils

from typing import Dict

app = Server()

app.add_file_route(
    file_path="resources/favicon.ico",
    content_type=ContentType.IMAGE,
    path="/favicon.ico",
)


@app.route()
def index(payload: str, headers: Dict[str, str], cookies: Dict[str, Cookie]) -> bytes:
    return FileUtils.template(
        path="resources/index.html",
        payload=payload,
        headers=repr(headers),
        cookies=repr(cookies),
    )


@app.route(path="/both")
@inject(cookies=True, headers=True)
def both() -> str:
    both.cookies.add(Cookie(name="test", value="123"))
    both.headers["test"] = "123"
    return "both"


@app.route(path="/cookie")
@inject(cookies=True)
def set_cookie() -> str:
    set_cookie.cookies.add(Cookie(name="test", value="123"))
    return "done"


@app.route(path="/styles.css", content_type=ContentType.CSS)
def styles() -> bytes:
    return FileUtils.read(path="resources/styles.css")


@app.route(path="/add", content_type=ContentType.HTML)
def add(a: str, b: str) -> str:
    result = int(a) + int(b)
    return f"<h1> Result = {result} </h1>"


@app.route(path="/division", content_type=ContentType.HTML)
def division() -> str:
    _ = 1 / 0
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


@app.route(path="/head")
@inject(headers=True)
def head() -> str:
    head.headers[HeaderType.CACHE_CONTROL.value] = str(
        CacheControl(public=True, max_age=timedelta(days=1))
    )

    return "head"


@app.route(path="/test", content_type=ContentType.HTML)
def test() -> Redirect:
    return Redirect(
        location="/", status_code=StatusCode.MOVED_PERMANENTLY, content="test123"
    )


if __name__ == "__main__":
    app.run()
