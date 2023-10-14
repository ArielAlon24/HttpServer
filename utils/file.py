import os


def read(path: str) -> bytes:
    if os.path.exists(path):
        with open(path, "rb") as file:
            return file.read()
    return b""
