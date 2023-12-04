"""
Name: Ariel Alon
Description:
    This module defines the 'StatusCode' tuple and related methods.
"""
from typing import NamedTuple


class StatusCode(NamedTuple):
    """
    A named tuple that represents an HTTP StatusCode.

    Attributes:
        code (int): status code's code.
        message (str): status code's message.
    """

    code: int
    message: str

    def __repr__(self) -> str:
        """
        A string representation of a status code.

        Returns:
            str: The string representation.
        """
        return f"{self.code} {self.message}"


OK = StatusCode(code=200, message="Ok")
BAD_REQUEST = StatusCode(code=400, message="Bad Request")
NOT_FOUND = StatusCode(code=404, message="Not Found")
INTERNAL_SERVER_ERROR = StatusCode(code=500, message="Internal Server Error")
CREATED = StatusCode(code=201, message="Created")
