from redis.asyncio import Redis

from domain.base.BaseUnitOfWork import BaseUnitOfWork
from repositories.redis.RedisUserRepository import RedisUserRepository


class RedisUnitOfWork(BaseUnitOfWork):
    def __init__(self, redis: Redis, prefix: str = "user:"):
        self._redis = redis
        self.user_repository = RedisUserRepository(redis, prefix)

    def __enter__(self) -> "RedisUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            pass

    def commit(self):
        pass

    def rollback(self):
        pass
