from ..enums.status_codes import StatusCode


class Redirect:
    def __init__(
        self,
        location: str,
        status_code: StatusCode = StatusCode.FOUND,
        content: str | bytes | None = None,
    ) -> None:
        self.location = location
        self.status_code = status_code
