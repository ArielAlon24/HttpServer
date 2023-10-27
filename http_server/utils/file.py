import os


def read(path: str) -> bytes:
    if os.path.exists(path):
        with open(path, "rb") as file:
            return file.read()
    return b""


def template(path: str, **kwargs: str) -> bytes:
    if not os.path.exists(path):
        return b""

    with open(path, "r") as template:
        content = template.read()

    for key, value in kwargs.items():
        content = content.replace(f"[{key}]", value)

    return content.encode()
