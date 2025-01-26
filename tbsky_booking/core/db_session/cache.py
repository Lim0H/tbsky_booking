from functools import cache

from redis import asyncio as aioredis

from tbsky_booking.core import AppSettings

__all__ = ["get_redis_connection"]


@cache
def get_redis_connection():
    return aioredis.from_url(str(AppSettings.database.REDIS_DSN))
