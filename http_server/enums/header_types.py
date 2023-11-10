"""
Name: Ariel Alon
Description:
    This module contains an enum for header types.
"""


from enum import Enum


class HeaderType(Enum):
    """
    An header type enum.
    """

    CONTENT_TYPE: str = "Content-Type"
    CONTENT_LENGTH: str = "Content-Length"
