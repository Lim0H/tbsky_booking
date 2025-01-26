from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["UsersSettings"]


class UsersSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="USERS_")

    DEFAULT_USER_ID: str
