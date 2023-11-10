"""
Name: Ariel Alon
Description:
    This module defines the 'StatusCode' class and related methods.
"""
from typing import Self


class StatusCode:
    """
    A class that represents an HTTP StatusCode.

    Attributes:
        code (int): status code's code.
        message (str): status code's message.
    """

    def __init__(self, code: int, message: str) -> None:
        """
        Initialize a StatusCode.

        Parameters:
            method (Method): Route's method.
            path (str): Route's path to resource.
        """
        self.code = code
        self.message = message

    @classmethod
    def ok(cls) -> Self:
        """
        Create an OK status code.

        Returns:
            StatusCode: OK status code.
        """
        return StatusCode(code=200, message="OK")

    @classmethod
    def bad_request(cls) -> Self:
        """
        Create an OK status code.

        Returns:
            StatusCode: OK status code.
        """
        return StatusCode(code=400, message="Bad Request")

    @classmethod
    def not_found(cls) -> Self:
        """
        Create an NotFound status code.

        Returns:
            StatusCode: NotFound status code.
        """
        return StatusCode(code=404, message="Not Found")

    @classmethod
    def internal_server_error(cls) -> Self:
        """
        Create an InternalServerError status code.

        Returns:
            StatusCode: InternalServerError status code.
        """
        return StatusCode(code=500, message="Internal Server Error")

    def __repr__(self) -> str:
        """
        A string representation of a status code.

        Returns:
            str: The string representation.
        """
        return f"{self.code} {self.message}"
