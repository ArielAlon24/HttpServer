from enum import Enum


class ContentType(Enum):
    HTML = "text/html; charset=utf-8"
    IMAGE = "image/jpeg"
    CSS = "text/css"
    JS = "text/javascript; charset=utf-8"
    JSON = "application/json"
    WOFF2 = "font/woff2"
    TTF = "font/ttf"
