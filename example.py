from http_server import HttpServer
from enums.content_types import ContentType
from utils import file

app = HttpServer()


@app.route(path="/favicon.ico", content_type=ContentType.IMAGE)
def favicon() -> bytes:
    return file.read(path="resources/favicon.ico")


@app.route(path="/", content_type=ContentType.HTML)
def index() -> bytes:
    return file.read(path="resources/index.html")


@app.route(path="/styles.css", content_type=ContentType.CSS)
def styles() -> bytes:
    return file.read(path="resources/styles.css")


@app.route(path="/script.js", content_type=ContentType.JS)
def script() -> bytes:
    return file.read(path="resources/script.js")


if __name__ == "__main__":
    app.run()
