from enum import Enum


class CookieAttribute(Enum):
    VALUE = "Value"
    MAX_AGE = "Max-Age"
    EXPIRES = "Expires"
    DOMAIN = "Domain"
    PATH = "Path"
    SECURE = "Secure"
    HTTP_ONLY = "HttpOnly"
    SAME_SITE = "SameSite"
