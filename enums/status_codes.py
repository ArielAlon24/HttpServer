from dataclasses import dataclass
from typing import Self


@dataclass
class StatusCode:
    code: int
    message: str

    @classmethod
    def ok(cls) -> Self:
        return StatusCode(code=200, message="OK")

    @classmethod
    def bad_request(cls) -> Self:
        return StatusCode(code=400, message="Bad Request")

    @classmethod
    def not_found(cls) -> Self:
        return StatusCode(code=404, message="Not Found")

    @classmethod
    def internal_server_error(cls) -> Self:
        return StatusCode(code=500, message="Internal Server Error")
