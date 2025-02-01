from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["DatabaseSettings"]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    DATABASE_URL: PostgresDsn = Field()
    REDIS_DSN: RedisDsn = Field()
