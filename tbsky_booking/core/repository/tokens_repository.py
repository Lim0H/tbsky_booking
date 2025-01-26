from ..models.security import BlackListToken
from .redis_repository import BaseRedisRepository

__all__ = ["BlackListTokenRepository"]


class BlackListTokenRepository(BaseRedisRepository[BlackListToken]):
    model = BlackListToken
