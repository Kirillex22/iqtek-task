from sqlmodel import Session

from domain.base.BaseUnitOfWork import BaseUnitOfWork
from repositories.postgres.PostgresUserRepository import PostgresUserRepository


class PostgresUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        self._session = session
        self.user_repository = PostgresUserRepository(session)

    async def commit(self):
        self._session.commit()

    async def rollback(self):
        self._session.rollback()

    async def __aenter__(self) -> "PostgresUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        self._session.close()
