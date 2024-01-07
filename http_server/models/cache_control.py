from datetime import timedelta


class CacheControl:
    def __init__(
        self,
        max_age: timedelta | None = None,
        s_maxage: timedelta | None = None,
        public: bool = False,
        private: bool = False,
        no_cache: bool = False,
        no_store: bool = False,
        must_revalidate: bool = False,
        proxy_revalidate: bool = False,
        immutable: bool = False,
        no_transform: bool = False,
        stale_while_revalidate: timedelta | None = None,
        stale_if_error: timedelta | None = None,
    ):
        self.max_age = max_age.total_seconds() if max_age is not None else None
        self.s_maxage = s_maxage.total_seconds() if s_maxage is not None else None
        self.public = public
        self.private = private
        self.no_cache = no_cache
        self.no_store = no_store
        self.must_revalidate = must_revalidate
        self.proxy_revalidate = proxy_revalidate
        self.immutable = immutable
        self.no_transform = no_transform
        self.stale_while_revalidate = (
            stale_while_revalidate.total_seconds()
            if stale_while_revalidate is not None
            else None
        )
        self.stale_if_error = (
            stale_if_error.total_seconds() if stale_if_error is not None else None
        )

    def __str__(self) -> str:
        parts = []
        for key, value in self.__dict__.items():
            if isinstance(value, bool):
                if value:
                    parts.append(key.replace("_", "-"))
            elif value is not None:
                parts.append(f"{key.replace('_', '-')}={int(value)}")
        return ", ".join(parts)
