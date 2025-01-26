from typing import Self

from pydantic import Field, PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["DatabaseSettings"]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    ASYNC_DATABASE_URI: PostgresDsn | str = Field(default="")
    DATABASE_USER: str = Field()
    DATABASE_PASSWORD: str = Field()
    DATABASE_HOST: str = Field()
    DATABASE_PORT: int = Field()
    DATABASE_NAME: str = Field()

    REDIS_DSN: RedisDsn = Field()

    @model_validator(mode="after")
    def assemble_db_connection(self) -> Self:
        self.ASYNC_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )
        return self
