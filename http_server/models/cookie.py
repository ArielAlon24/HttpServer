from datetime import datetime
from ..utils.date import DateUtils


class Cookie:
    SAME_SITE_OPTIONS = ["Strict", "Lax"]

    def __init__(
        self,
        name: str,
        value: str,
        max_age: int | None = None,
        expires: datetime | None = None,
        domain: str | None = None,
        path: str = "/",
        secure: bool = False,
        http_only: bool = False,
        same_site: str | None = None,
    ):
        self.name = name
        self.value = value
        self.max_age = max_age
        self.expires = expires
        self.domain = domain
        self.path = path
        self.secure = secure
        self.http_only = http_only

        if same_site and same_site not in ["Lax", "Strict"]:
            raise ValueError(
                "same_site attribute must be one of the following"
                + f" 'Lax', 'Strict' or None"
            )
        self.same_site = same_site

    def __str__(self) -> str:
        cookie = f"{self.name}={self.value}; Path={self.path}"
        if self.max_age:
            cookie += f"; Max-Age={self.max_age}"
        if self.expires:
            cookie += f"; Expires={DateUtils.rfc7321(self.expires)}"
        if self.domain:
            cookie += f"; Domain={self.domain}"
        if self.secure:
            cookie += "; Secure"
        if self.http_only:
            cookie += "; HttpOnly"
        if self.same_site:
            cookie += f"; SameSite={self.same_site}"
        return cookie

    def __repr__(self) -> str:
        return (
            f"Cookie(name='{self.name}', "
            f"value='{self.value}', "
            f"path='{self.path}', "
            f"secure={self.secure}, "
            f"http_only={self.http_only}, "
            f"same_site='{self.same_site}')"
        )
