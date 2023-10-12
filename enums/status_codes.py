from dataclasses import dataclass


@dataclass
class StatusCode:
    code: int
    message: str


OK = StatusCode(code=200, message="OK")
BAD_REQUEST = StatusCode(code=400, message="Bad Request")
NOT_FOUND = StatusCode(code=404, message="Not Found")
