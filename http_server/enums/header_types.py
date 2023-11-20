"""
Name: Ariel Alon
Description:
    This module contains an enum for header types.
"""


from enum import Enum


class HeaderType(Enum):
    """
    An http header type enum.
    """

    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
    DATE = "Date"
