class FileUtils:
    @staticmethod
    def read(path: str) -> bytes:
        with open(path, "rb") as file:
            return file.read()

    @staticmethod
    def template(path: str, **kwargs: str) -> bytes:
        with open(path, "r") as template:
            content = template.read()

        for key, value in kwargs.items():
            content = content.replace(f"[{key}]", value)

        return content.encode()
