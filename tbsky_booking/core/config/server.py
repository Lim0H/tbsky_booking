from pydantic import AnyUrl, Field, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["ServerSettings"]


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SERVER_")

    HOST: IPvAnyAddress | AnyUrl = Field(default="127.0.0.1")  # type: ignore
    PORT: int = Field(default=8088, ge=0, le=65535)
