"""
Description:
    This module has date related utility functions.
"""
from datetime import datetime, timezone


def rfc7321() -> str:
    """
    get the current datetime formmated in the rfc7321 format.

    Returns:
        datetime (str): The datetime formatted
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%a, %d %b %Y %H:%M:%S GMT")
