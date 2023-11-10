"""
Name: Ariel Alon
Description:
    This module defines the 'Route' class and related methods.
"""
from ..enums.methods import Method

from typing import Self


class Route:
    """
    A class that represents an HTTP route

    Attributes:
        method (Method): Route's method.
        path (str): Route's path to resource.
    """

    def __init__(self, method: Method, path: str) -> None:
        """
        Initialize a Resource.

        Parameters:
            method (Method): Route's method.
            path (str): Route's path to resource.
        """
        self.method = method
        self.path = path

    def __hash__(self) -> int:
        """
        Hash a route instance. Used for using a Route as a dictionary key.

        Returns:
            int: The hash value.
        """
        return hash((self.method, self.path))

    def __eq__(self, other: Self) -> bool:
        """
        Compare route instances. Used for using a Route as a dictionary key.

        Returns:
            bool: Are self and other Routes are equal.
        """
        if not isinstance(other, Route):
            return False
        return self.method == other.method and self.path == other.path

    def __repr__(self) -> str:
        """
        A string representation of a Route.

        Returns:
            str: The string representation.
        """
        return f"'{self.method.value} {self.path}'"
