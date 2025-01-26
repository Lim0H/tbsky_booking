import asyncio
import logging
from abc import ABC
from functools import cached_property, lru_cache
from typing import TypeVar

import httpx
from fake_useragent import UserAgent

from ..schema import BaseSchema
from .abc_repository import EmptyRepository, GetRepository

__all__ = ["BaseGetRestApiRepository", "BaseRestApiRepository"]


T = TypeVar("T", bound=BaseSchema)

log = logging.getLogger(__file__)


@lru_cache
def get_global_requests_client():
    ua = UserAgent()

    return httpx.AsyncClient(
        timeout=httpx.Timeout(120),
        headers={
            "User-Agent": ua.chrome,
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://www.google.com/",
        },
        limits=httpx.Limits(max_connections=10000, max_keepalive_connections=10000),
    )


class BaseRestApiRepository(EmptyRepository[T]):

    @cached_property
    def requests_client(self):
        return get_global_requests_client()


class BaseGetRestApiRepository(BaseRestApiRepository[T], GetRepository[T], ABC):
    async def __call__(self, *args, **kwargs):
        return await self.get(*args, **kwargs)
