from enum import Enum


class HeaderType(Enum):
    CONTENT_TYPE: str = "Content-Type"
    CONTENT_LENGTH: str = "Content-Length"
