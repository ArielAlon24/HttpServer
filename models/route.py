from typing import Self
from ..enums.methods import Method


class Route:
    def __init__(self, method: Method, path: str) -> Self:
        self.method = method
        self.path = path

    def __hash__(self) -> int:
        return hash((self.method, self.path))

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Route):
            return False
        return self.method == other.method and self.path == other.path
