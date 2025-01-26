from typing import Optional

from pydantic import HttpUrl
from sqlalchemy import String, TypeDecorator

__all__ = ["HttpUrlType"]


class HttpUrlType(TypeDecorator):
    impl = String(2083)
    cache_ok = True
    python_type = HttpUrl

    def process_bind_param(
        self, value: Optional[str], dialect
    ) -> Optional[str]:
        return str(value) if value else None

    def process_result_value(
        self, value: Optional[str], dialect
    ) -> Optional[HttpUrl]:
        return HttpUrl(url=value) if value else None

    def process_literal_param(self, value: str, dialect) -> str:
        return str(value)
