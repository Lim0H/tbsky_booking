import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlmodel import Field

from tbsky_booking.core.config import AppSettings

from ..schema import BaseSchema
from ..types.model import PrimaryKeyType

__all__ = ["make_primary_key", "BaseModel"]


def make_primary_key() -> PrimaryKeyType:
    return Field(default_factory=uuid.uuid4, primary_key=True)


class BaseModel(BaseSchema):
    created_by: str = Field(default_factory=lambda: AppSettings.users.DEFAULT_USER_ID)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={"default": func.now()},
    )  # type: Ignore
    updated_by: Optional[str] = Field(default=None)
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={"default": None, "onupdate": func.now()},
    )  # type: Ignore
    deleted: bool = Field(default=False)
