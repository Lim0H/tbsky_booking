import uuid
from datetime import datetime

from pydantic import Field

from ..config import AppSettings
from ..schema import BaseSchema

__all__ = ["BaseRedisModel"]


class BaseRedisModel(BaseSchema):
    key: str = Field(default_factory=lambda: str(uuid.uuid4()))

    created_by: str = Field(default_factory=lambda: AppSettings.users.DEFAULT_USER_ID)
    created_at: datetime = Field(default_factory=datetime.now)
