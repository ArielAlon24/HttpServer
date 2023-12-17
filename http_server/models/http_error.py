from ..enums.status_code import StatusCode


class HttpError(Exception):
    def __init__(
        self,
        message: str,
        status_code: StatusCode,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
