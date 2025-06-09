from sqlalchemy.exc import IntegrityError

from src.common.base.BaseSessionFactory import BaseSessionFactory
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.repositories.postgres.SQLAlchemyUserRepository import SQLAlchemyUserRepository
from src.common.exceptions.UserServiceExceptions import UserAlreadyExistsException

class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    def __init__(self, session_factory: BaseSessionFactory):
        self._session_factory = session_factory

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = self._session_factory.get_session()
        self.user_repository = SQLAlchemyUserRepository(self._session)
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
