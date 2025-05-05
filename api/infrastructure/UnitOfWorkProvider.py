from redis.asyncio import Redis
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from config.Config import DBType, Config
from domain.base.BaseUnitOfWork import BaseUnitOfWork
from repositories.postgres.PostgresUOW import PostgresUnitOfWork
from repositories.redis.RedisUOW import RedisUnitOfWork


class UnitOfWorkProvider:
    def __init__(self, config: Config):
        self.config = config

    def get_uow(self) -> BaseUnitOfWork:
        db_type = self.config.db_type

        if db_type == DBType.POSTGRESQL:
            return self._get_postgres_uow()
        elif db_type == DBType.REDIS:
            return self._get_redis_uow()

    def _get_postgres_uow(self) -> PostgresUnitOfWork:
        database_url = self.config.postgres_data.generate_url()
        engine = create_engine(database_url)
        SQLModel.metadata.create_all(engine)
        session = Session(engine)

        return PostgresUnitOfWork(session)

    def _get_redis_uow(self) -> RedisUnitOfWork:
        redis_url = self.config.redis_data.generate_url()
        redis = Redis.from_url(redis_url, password=self.config.redis_data.password)

        return RedisUnitOfWork(redis)
