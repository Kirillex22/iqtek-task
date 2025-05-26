from typing import Optional, Union

from redis import Redis
from sqlmodel import Session

from src.common.base.BaseSessionFactory import BaseSessionFactory
from src.config.Config import DBType, Config
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.infrastructure.RedisSessionFactory import RedisSessionFactory
from src.infrastructure.SQLModelSessionFactory import SQLModelSessionFactory
from src.plugins.user.repositories.postgres.PostgresUOW import PostgresUnitOfWork
from src.plugins.user.repositories.redis.RedisUOW import RedisUnitOfWork


class UnitOfWorkProvider:
    def __init__(self, config: Config, client: Optional[Union[Session, Redis]] = None):
        self.config = config
        self.client = client
        self.session_factory = None

    def get_uow(self) -> Optional[BaseUnitOfWork]:
        db_type = self.config.db_type

        if db_type == DBType.POSTGRESQL:
            if self.config.postgres_data:
                db_url = self.config.postgres_data.generate_url()
                self.session_factory = SQLModelSessionFactory(db_url)

            return self._get_postgres_uow()
        elif db_type == DBType.REDIS:
            if self.config.redis_data:
                db_url = self.config.redis_data.generate_url()
                self.session_factory = RedisSessionFactory(db_url, self.config.redis_data.password)
            return self._get_redis_uow()
        return None

    def _get_postgres_uow(self) -> PostgresUnitOfWork:
        if self.client:
            session = self.client
        else:
            session = self.session_factory.get_session()
        return PostgresUnitOfWork(session)

    def _get_redis_uow(self) -> RedisUnitOfWork:

        if self.client:
            redis = self.client
        else:
            redis = self.session_factory.get_session()
        return RedisUnitOfWork(redis)
