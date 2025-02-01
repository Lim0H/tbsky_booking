from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .database import DatabaseSettings
from .performance import PerformanceSettings
from .security import SecuritySettings
from .server import ServerSettings
from .users import UsersSettings

__all__ = ["AppSettings"]

load_dotenv()


class _AppSettings(BaseSettings):
    performance: PerformanceSettings = PerformanceSettings()
    database: DatabaseSettings = DatabaseSettings()
    users: UsersSettings = UsersSettings()
    security: SecuritySettings = SecuritySettings()
    server: ServerSettings = ServerSettings()


AppSettings = _AppSettings()
