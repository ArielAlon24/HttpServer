from ..enums import ContentType, StatusCode
from ..types import Creator


class Resource:
    def __init__(
        self,
        function: Creator,
        content_type: ContentType,
        success_status: StatusCode,
    ) -> None:
        self.function = function
        self.content_type = content_type
        self.success_status = success_status
