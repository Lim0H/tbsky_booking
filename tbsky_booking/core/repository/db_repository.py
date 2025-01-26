import logging
from abc import ABC
from contextlib import _AsyncGeneratorContextManager
from typing import Any, Callable, Iterable, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from tbsky_booking.core.db_session.postgres import get_async_session
from tbsky_booking.core.repository.abc_repository import GenericRepository
from tbsky_booking.core.schema import BaseSchema

from ..models import BaseModel

log = logging.getLogger(__file__)

__all__ = ["BaseDbRepository"]


MODEL_VAR = TypeVar("MODEL_VAR", bound=BaseModel)
EDIT_MODEL_VAR = TypeVar("EDIT_MODEL_VAR", bound=BaseSchema)


class BaseDbRepository(GenericRepository[MODEL_VAR], ABC):
    model: Type[MODEL_VAR]

    async_session_factory: Callable[
        ..., _AsyncGeneratorContextManager[AsyncSession]
    ] = get_async_session

    async def _callback_before_add(self, obj_new: MODEL_VAR) -> MODEL_VAR:
        return obj_new

    async def _add(
        self,
        obj_new: MODEL_VAR,
        db_session: AsyncSession,
        with_commmit=False,
    ) -> MODEL_VAR:
        """Commit new object to the database."""
        obj_new = await self._callback_before_add(obj_new)
        try:
            db_session.add(obj_new)
            await db_session.flush()
            if with_commmit:
                await db_session.commit()
            await db_session.refresh(obj_new)
            log.debug(f"Created new entity: {obj_new}.")
            return obj_new
        except Exception:
            log.exception("Error while uploading new object to database")
            raise

    async def add(
        self,
        obj_new: MODEL_VAR,
        session: Optional[AsyncSession] = None,
        with_commmit=False,
    ) -> MODEL_VAR:
        """Commit new object to the database."""
        obj_new = await self._callback_before_add(obj_new)
        if session:
            return await self._add(obj_new, session, with_commmit)
        try:
            async with self.async_session_factory() as db_session:
                return await self._add(obj_new, db_session, with_commmit)
        except Exception:
            log.exception("Error while uploading new object to database")
            raise

    async def add_massive(self, models: Iterable[MODEL_VAR]) -> list[MODEL_VAR]:
        added_models: list[MODEL_VAR] = []
        async with self.async_session_factory() as db_session:
            for model in models:
                await self.add(model, session=db_session, with_commmit=False)
            await db_session.commit()
        log.info(
            f"Added {len(models) if hasattr(models, '__len__') else ''} models to database"
        )
        return added_models

    async def get(
        self, params: Optional[dict[Any, list | Any]] = None
    ) -> list[MODEL_VAR]:
        params = {} if not params else params
        async with self.async_session_factory() as db_session:
            q = select(self.model).filter(col(self.model.deleted).is_(False))
            for col_name, value in params.items():
                col_field = getattr(self.model, col_name)
                if any(map(lambda x: isinstance(value, x), [list, set, tuple])):
                    q = q.filter(col(col_field).in_(value))
                elif value is None:
                    q = q.filter(col(col_field).is_(value))
                else:
                    q = q.filter(col(col_field) == value)
            return (await db_session.execute(q)).scalars().all()
