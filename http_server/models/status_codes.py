from typing import Self


class StatusCode:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

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

    def __repr__(self) -> str:
        return f"{self.code} {self.message}"
