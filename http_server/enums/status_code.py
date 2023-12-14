"""
Description:
    This module contains an enum for HTTP status codes.
"""

from enum import Enum


class StatusCode(Enum):
    """
    Enum representing HTTP Status Codes.
    """

    OK = (200, "Ok")
    BAD_REQUEST = (400, "Bad Request")
    NOT_FOUND = (404, "Not Found")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    CREATED = (201, "Created")
    MOVED_PERMANENTLY = (301, "Moved Permanently")
    FOUND = (302, "Found")

    def __init__(self, code: int, message: str):
        """
        Initialize a StatusCode.

        Parameters:
            code (int): Status code's code.
            message (str): Status code's message.
        """
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        """
        A string representation of a status code.

        Returns:
            str: The string representation.
        """
        return f"{self.code} {self.message}"
