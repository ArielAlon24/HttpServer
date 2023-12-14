"""
Description:
    This module defines the 'Redirect' class.
"""

from ..enums.status_code import StatusCode


class Redirect:
    def __init__(
        self, location: str, status_code: StatusCode = StatusCode.FOUND
    ) -> None:
        """
        Initialize a resource.

        Parameters:
            location (str): location to redirect to.
            status_code (StatusCode): Status code returned upon redirection.
        """
        self.location = location
        self.status_code = status_code
