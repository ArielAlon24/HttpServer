"""
Name: Ariel Alon
Description: This module has file related utility functions.
"""

import os


def read(path: str) -> bytes:
    """
    Read the content of a file.

    Parameters:
        path (str): The path to the file.

    Returns:
        bytes: The file's content.
    """
    if os.path.exists(path):
        with open(path, "rb") as file:
            return file.read()
    return b""


def template(path: str, **kwargs: str) -> bytes:
    """
    Use a template file with [variable] markup.
    Reads the contents of a file located in a specified path,
    and replaces all key in the

    Parameters:
        path (str): The path to the file.

    Returns:
        bytes: The template after key-value replacement.
    """
    if not os.path.exists(path):
        return b""

    with open(path, "r") as template:
        content = template.read()

    for key, value in kwargs.items():
        content = content.replace(f"[{key}]", value)

    return content.encode()
