"""
Name: Ariel Alon
Description:
    This module has html related utility functions.
"""


def string_to_html(string: str) -> str:
    """
    Convert special characters into html escaped characters.

    Parameters:
        string (str): The entire html string.

    Returns:
        str: the html string with characters escaped.
    """
    replacements = {
        "&": "&amp;",
        "'": "&#39;",
        '"': "&quot;",
        "\t": "&emsp;",
        "<": "&lt;",
        ">": "&gt;",
        "\n": "<br>",
    }

    for escape, html in replacements.items():
        string = string.replace(escape, html)

    return string
