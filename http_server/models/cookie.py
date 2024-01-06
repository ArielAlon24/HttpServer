from datetime import datetime
from ..utils.date import DateUtils


class Cookie:
    SAME_SITE_OPTIONS = ["Strict", "Lax"]

    def __init__(
        self,
        name: str,
        value: str,
        expires: datetime | None = None,
        domain: str | None = None,
        path: str = "/",
        secure: bool = False,
        httponly: bool = False,
        samesite: str | None = None,
    ):
        if not name or not value:
            raise ValueError("name and value attributes must be non empty.")

        self.name = name
        self.value = value
        self.expires = expires
        self.domain = domain
        self.path = path
        self.secure = secure
        self.http_only = httponly

        if samesite and samesite not in ["Lax", "Strict"]:
            raise ValueError(
                "same_site attribute must be one of the following"
                + f" 'Lax', 'Strict' or None"
            )
        self.same_site = samesite

    def __str__(self) -> str:
        cookie = f"{self.name}={self.value}; Path={self.path}"
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
            f"expires='{self.expires}', "
            f"domain='{self.domain}', "
            f"secure={self.secure}, "
            f"http_only={self.http_only}, "
            f"same_site='{self.same_site}')"
        )

    def __hash__(self):
        return hash(
            (
                self.name,
                self.value,
                self.domain,
                self.path,
                self.secure,
                self.http_only,
                self.same_site,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, Cookie):
            return False

        return (
            self.name == other.name
            and self.value == other.value
            and self.expires == other.expires
            and self.domain == other.domain
            and self.path == other.path
            and self.secure == other.secure
            and self.http_only == other.http_only
            and self.same_site == other.same_site
        )
