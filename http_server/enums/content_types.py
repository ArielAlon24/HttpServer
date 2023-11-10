"""
Name: Ariel Alon
Description:
    This module contains an enum for content types.
"""

from enum import Enum


class ContentType(Enum):
    """
    A content type enum.
    """

    HTML: str = "text/html; charset=utf-8"
    IMAGE: str = "image/jpeg"
    CSS: str = "text/css"
    JS: str = "text/javascript; charset=utf-8"
    JSON: str = "application/json"
