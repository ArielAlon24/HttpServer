"""
Name: Ariel Alon
Description: This module defines the 'Resource' class.
"""

from ..enums.content_types import ContentType

from typing import Callable, Tuple


class Resource:
    """
    A class that represents a Resource.

    Attributes:
        function (Callable[Tuple, str]): The content creating function.
        content_type (ContentType): The content type of the resource.
    """

    def __init__(
        self, function: Callable[Tuple, str], content_type: ContentType
    ) -> None:
        """
        Initialize a resource.

        Parameters:
            function (Callable[Tuple, str]): The content creating function.
            content_type (ContentType): The content type of the resource.
        """
        self.function = function
        self.content_type = content_type
