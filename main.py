from http_server import HttpServer
from enums.content_types import ContentType

app = HttpServer()


@app.route(path="/favicon.ico", content_type=ContentType.IMAGE)
def favicon() -> bytes:
    with open("favicon.ico", "rb") as file:
        content = file.read()
    return content


@app.route(path="/")
def index() -> str:
    return "<h1>Welcome!</h1>"


if __name__ == "__main__":
    app.run()
