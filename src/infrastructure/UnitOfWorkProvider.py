from typing import Optional

from src.common.exceptions.InfrastructureExceptions import ConfigurationException
from src.config.Config import DBType, Config
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.repositories.redis.RedisSessionFactory import RedisSessionFactory
from src.plugins.user.repositories.postgres.SQLAlchemySessionFactory import SQLAlchemySessionFactory
from src.plugins.user.orm.UserORM import register_map
from src.plugins.user.repositories.postgres.SQLAlchemyUOW import SQLAlchemyUnitOfWork
from src.plugins.user.repositories.redis.RedisUOW import RedisUnitOfWork


class UnitOfWorkProvider:
    def __init__(self, config: Config, client = None):
        self.config = config
        self.client = client
        self.session_factory = None

    def get_uow(self) -> Optional[BaseUnitOfWork]:
        db_type = self.config.db_type

        if db_type == DBType.POSTGRESQL:
            if self.config.postgres_data and not self.session_factory:
                db_url = self.config.postgres_data.generate_url()
                self.session_factory = SQLAlchemySessionFactory(db_url)
                register_map(self.session_factory.get_engine()) # инит орм для users

            return self._get_postgres_uow()

        elif db_type == DBType.REDIS:
            if self.config.redis_data and not self.session_factory:
                db_url = self.config.redis_data.generate_url()
                self.session_factory = RedisSessionFactory(db_url, self.config.redis_data.password)

            return self._get_redis_uow()

        raise ConfigurationException(f"Указанный тип БД не поддерживается.")

    def _get_postgres_uow(self) -> SQLAlchemyUnitOfWork:
        if self.client:
            session_factory = self.client
        else:
            session_factory = self.session_factory
        return SQLAlchemyUnitOfWork(session_factory)

    def _get_redis_uow(self) -> RedisUnitOfWork:

        if self.client:
            redis_factory = self.client
        else:
            redis_factory = self.session_factory

        return RedisUnitOfWork(redis_factory)
