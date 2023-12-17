from enum import Enum


class HeaderType(Enum):
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
    LOCATION = "Location"
    DATE = "Date"
    COOKIE = "Cookie"
    SET_COOKIE = "Set-Cookie"
