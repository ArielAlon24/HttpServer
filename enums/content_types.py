from enum import Enum


class ContentType(Enum):
    HTML: str = "text/html; charset=utf-8"
    IMAGE: str = "image/jpeg"
    CSS: str = "text/css"
    JS: str = "text/javascript; charset=utf-8"
    JSON: str = "application/json"
