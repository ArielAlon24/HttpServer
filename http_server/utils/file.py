"""
Name: Ariel Alon
Description:
    This module has file related utility functions.
    Note: It can raise any Exceptions regarding files,
    they are handled in the client_handler.
"""


def read(path: str) -> bytes:
    """
    Read the content of a file.

    Parameters:
        path (str): The path to the file.

    Returns:
        bytes: The file's content.
    """
    with open(path, "rb") as file:
        return file.read()


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
    with open(path, "r") as template:
        content = template.read()

    for key, value in kwargs.items():
        content = content.replace(f"[{key}]", value)

    return content.encode()
