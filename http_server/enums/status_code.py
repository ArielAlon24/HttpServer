from enum import Enum


class StatusCode(Enum):
    OK = (200, "Ok")
    BAD_REQUEST = (400, "Bad Request")
    NOT_FOUND = (404, "Not Found")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    CREATED = (201, "Created")
    MOVED_PERMANENTLY = (301, "Moved Permanently")
    FOUND = (302, "Found")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        return f"{self.code} {self.message}"
