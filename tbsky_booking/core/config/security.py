from typing import Literal

from pydantic import Field, SecretBytes, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["SecuritySettings"]


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SECURITY_")

    SECRET_KEY: SecretStr
    CRYPTO_KEY: SecretBytes
    JWT_ALGORITHM: Literal["HS256", "HS384", "HS512"] = Field(default="HS256")
