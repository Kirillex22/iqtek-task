from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.repositories.postgres.PostgresUserRepository import PostgresUserRepository
from src.common.exceptions.UserServiceExceptions import UserAlreadyExistsException

class PostgresUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        self._session = session
        self.user_repository = PostgresUserRepository(session)

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    def __enter__(self) -> "PostgresUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()

        else:
            try:
                self.commit()
            except IntegrityError:
                raise UserAlreadyExistsException()

        self._session.close()
