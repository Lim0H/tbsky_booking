import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asyncpg import TooManyConnectionsError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from ..config import AppSettings

log = logging.getLogger(__file__)

__all__ = [
    "get_async_engine",
    "initialize_database",
    "get_async_session",
]


def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    try:
        async_engine: AsyncEngine = create_async_engine(
            str(AppSettings.database.ASYNC_DATABASE_URI),
            future=True,
            # echo=True,
        )
    except SQLAlchemyError:
        log.warning(
            "Unable to establish db engine, database might not exist yet",
            exc_info=True,
        )
        raise

    return async_engine


async def initialize_database() -> None:
    """Create table in metadata if they don't exist yet.

    This uses a sync connection because the 'create_all' doesn't
    feature async yet.
    """
    from tbsky_booking import models  # noqa

    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:
        from sqlmodel import SQLModel

        await async_conn.run_sync(SQLModel.metadata.create_all)
        log.info("Initializing database was successfull.")


@asynccontextmanager
@retry(
    retry=retry_if_exception_type(TooManyConnectionsError),
    stop=stop_after_attempt(100),
    wait=wait_fixed(5),
)
async def get_async_session(
    in_transaction: bool = False,
    *args,
    **kwargs,
) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session.

    All conversations with the database are established via the session
    objects. Also. the sessions act as holding zone for ORM-mapped objects.
    """
    AsyncSessionFactory = async_sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    async with AsyncSessionFactory() as session:
        try:
            if in_transaction:
                async with session.begin():
                    yield session
            else:
                yield session
            await session.close()
        except SQLAlchemyError:
            await session.close()
            log.error("Unable to yield session in database dependency")
            raise
