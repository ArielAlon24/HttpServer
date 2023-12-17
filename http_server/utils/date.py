from datetime import datetime, timezone


class DateUtils:
    @staticmethod
    def rfc7321(date: datetime = datetime.now(timezone.utc)) -> str:
        return date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def from_rfc7321(string: str) -> datetime:
        return datetime.strptime(string, "%a, %d-%b-%Y %H:%M:%S GMT")
