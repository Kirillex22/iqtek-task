from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.repositories.redis.RedisSessionFactory import RedisSessionFactory
from src.plugins.user.repositories.redis.RedisUserRepository import RedisUserRepository


class RedisUnitOfWork(BaseUnitOfWork):
    def __init__(self, redis_factory: RedisSessionFactory, prefix: str = "user:"):
        self._prefix = prefix
        self._redis_factory = redis_factory


    def __enter__(self) -> "RedisUnitOfWork":
        self._session = self._redis_factory.get_session()
        self.user_repository = RedisUserRepository(self._session, prefix=self._prefix)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            pass

    def commit(self):
        pass

    def rollback(self):
        pass
