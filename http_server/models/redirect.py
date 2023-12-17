from ..enums.status_code import StatusCode


class Redirect:
    def __init__(
        self, location: str, status_code: StatusCode = StatusCode.FOUND
    ) -> None:
        self.location = location
        self.status_code = status_code
