"""
Description:
    This module defines the 'Resource' class.
"""

from ..enums.content_types import ContentType
from ..enums.status_code import StatusCode

from typing import Callable


class Resource:
    """
    A class that represents a Resource.

    Attributes:
        function (Callable[..., str | bytes | None]):
            The content creating function.
        content_type (ContentType):
            The content type of the resource.
        success_status (StatusCode):
            Status code returned upon success
    """

    def __init__(
        self,
        function: Callable[..., str | bytes | None],
        content_type: ContentType,
        success_status: StatusCode,
    ) -> None:
        """
        Initialize a resource.

        Parameters:
            function (Callable[..., str | bytes | None]): The content creating function.
            content_type (ContentType): The content type of the resource.
            success_status (StatusCode): Status code returned upon success.
        """
        self.function = function
        self.content_type = content_type
        self.success_status = success_status
