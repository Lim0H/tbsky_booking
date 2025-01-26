from typing import Literal, TypeAlias

from pydantic import Field, model_validator

from ..schema import BaseSchema
from .redis_model import BaseRedisModel

__all__ = ["Token", "TokenBase", "BlackListToken"]

TOKEN_TYPE: TypeAlias = Literal["bearer", "blacklist"]


class TokenBase(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: TOKEN_TYPE = Field(default="bearer")


class Token(TokenBase, BaseRedisModel):
    token_type: TOKEN_TYPE = Field(default="bearer")


class BlackListToken(Token):
    token_type: TOKEN_TYPE = Field(default="blacklist")

    @model_validator(mode="after")
    def after_validation(self):
        self.key = self.access_token
        return self
