"""
Name: Ariel Alon
Description:
    This module defines the 'HttpError' exception.
"""

from .status_code import StatusCode


class HttpError(Exception):
    """
    An exception class for all Http realted exceptions.

    Attributes:
        message (str): Excpetion message.
        status_code (StatusCode): Exception's http status code.
    """

    def __init__(
        self,
        message: str,
        status_code: StatusCode,
    ) -> None:
        """
        Initialize an HttpError.
        """
        super().__init__(message)
        self.status_code = status_code
