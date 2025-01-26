from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from tbsky_booking.core import get_redis_connection

from .v1 import routers

__all__ = ["init_fastapi_server"]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = get_redis_connection()
    print(f"Connected to redis: {await redis.ping()}")
    FastAPICache.init(RedisBackend(redis), prefix="tbsky-bookings")
    yield


def init_fastapi_server() -> FastAPI:
    app = FastAPI(title="TBSky Booking Service", lifespan=lifespan)

    for router in routers:
        app.include_router(router, prefix="/api/v1")

    return app


async def run_fastapi_server():
    app = init_fastapi_server()

    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    await server.serve()
