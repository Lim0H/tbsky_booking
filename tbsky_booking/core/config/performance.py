from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["PerformanceSettings"]


class PerformanceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PERFORMANCE_")

    MAX_WORKER_NUMBER: int = Field(default=5, le=10)
