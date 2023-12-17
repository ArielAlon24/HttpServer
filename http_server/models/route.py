from ..enums.methods import Method


class Route:
    def __init__(self, method: Method, path: str) -> None:
        self.method = method
        self.path = path

    def __hash__(self) -> int:
        return hash((self.method, self.path))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Route):
            return False
        return self.method == other.method and self.path == other.path

    def __repr__(self) -> str:
        return f"'{self.method.value} {self.path}'"
