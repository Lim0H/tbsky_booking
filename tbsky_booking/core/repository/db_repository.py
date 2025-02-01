import logging
from abc import ABC
from contextlib import _AsyncGeneratorContextManager
from typing import Any, Callable, Iterable, Optional, Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from tbsky_booking.core.config import AppSettings
from tbsky_booking.core.db_session.postgres import get_async_session
from tbsky_booking.core.models import BaseModel
from tbsky_booking.core.repository.abc_repository import GenericRepository
from tbsky_booking.core.schema import BaseSchema

from ..depends.security import get_user_id_by_access_token

log = logging.getLogger(__file__)

__all__ = ["BaseDbRepository"]


MODEL_VAR = TypeVar("MODEL_VAR", bound=BaseModel)
EDIT_MODEL_VAR = TypeVar("EDIT_MODEL_VAR", bound=BaseSchema)


class BaseDbRepository(GenericRepository[MODEL_VAR], ABC):
    model: Type[MODEL_VAR]
    user_id: str = AppSettings.users.DEFAULT_USER_ID

    async_session_factory: Callable[
        ..., _AsyncGeneratorContextManager[AsyncSession]
    ] = get_async_session

    def __init__(
        self,
        user_id: str = Depends(get_user_id_by_access_token),
    ):
        self.user_id = user_id

    async def _callback_before_add(self, model: MODEL_VAR) -> MODEL_VAR:
        return model

    async def _callback_before_edit(self, model: MODEL_VAR) -> MODEL_VAR:
        return model

    async def _add(
        self,
        model: MODEL_VAR,
        db_session: AsyncSession,
        with_commmit=False,
    ) -> MODEL_VAR:
        """Commit new object to the database."""
        model = await self._callback_before_add(model)
        model.created_by = self.user_id
        try:
            db_session.add(model)
            await db_session.flush()
            if with_commmit:
                await db_session.commit()
            await db_session.refresh(model)
            log.debug(f"Created new entity: {model}.")
            return model
        except Exception:
            log.exception("Error while uploading new object to database")
            raise

    async def add(
        self,
        model: MODEL_VAR,
        session: Optional[AsyncSession] = None,
        with_commmit=False,
    ) -> MODEL_VAR:
        """Commit new object to the database."""
        model = await self._callback_before_add(model)
        if session:
            return await self._add(model, session, with_commmit)
        try:
            async with self.async_session_factory() as db_session:
                return await self._add(model, db_session, with_commmit)
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
                if isinstance(value, (list, set, tuple)):
                    q = q.filter(col(col_field).in_(value))
                elif value is None:
                    q = q.filter(col(col_field).is_(value))
                else:
                    q = q.filter(col(col_field) == value)
            q = q.order_by(col(self.model.created_at).desc())
            return list((await db_session.execute(q)).scalars().all())

    async def _edit(
        self,
        model: MODEL_VAR,
        session: AsyncSession,
        with_commmit=False,
    ) -> MODEL_VAR:
        model.updated_by = self.user_id
        return await self._add(model, session, with_commmit)

    async def edit(
        self,
        model: MODEL_VAR,
        session: Optional[AsyncSession] = None,
        with_commmit=False,
    ) -> MODEL_VAR:
        """Commit new object to the database."""
        model = await self._callback_before_edit(model)
        if session:
            return await self._edit(model, session, with_commmit)
        try:
            async with self.async_session_factory() as db_session:
                return await self._edit(model, db_session, with_commmit)
        except Exception:
            log.exception("Error while uploading new object to database")
            raise

    async def merge(
        self,
        model: MODEL_VAR,
        schema: EDIT_MODEL_VAR,
        session: Optional[AsyncSession] = None,
        with_commmit=False,
    ) -> MODEL_VAR:
        for attr, value in schema.model_dump(exclude_unset=True).items():
            if not hasattr(model, attr):
                raise AttributeError(f"Model {model} has no attribute {attr}")
            if getattr(model, attr) != value:
                setattr(model, attr, value)
        return await self.edit(model, session=session, with_commmit=with_commmit)
