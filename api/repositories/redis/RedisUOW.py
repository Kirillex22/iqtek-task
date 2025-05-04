from redis.asyncio import Redis

from domain.base.BaseUnitOfWork import BaseUnitOfWork
from repositories.redis.RedisUserRepository import RedisUserRepository


class RedisUnitOfWork(BaseUnitOfWork):
    def __init__(self, redis: Redis, prefix: str = "user:"):
        self._redis = redis
        self.user_repository = RedisUserRepository(redis, prefix)

    async def __aenter__(self) -> "RedisUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            pass

    async def commit(self):
        pass

    async def rollback(self):
        pass
