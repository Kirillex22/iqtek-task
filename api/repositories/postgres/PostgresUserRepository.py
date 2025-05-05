from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from domain.base.BaseUserRepository import BaseUserRepository
from domain.entities.User import User
from repositories.postgres.Mappers import map_user_model_to_orm, map_user_orm_to_model
from repositories.postgres.orm.UserORM import UserORM
from shared.exceptions.UserServiceExceptions import UserNotExistsException, UnknownUserException


class PostgresUserRepository(BaseUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def create_user(self, user: User) -> None:
        try:
            self._session.add(
                map_user_model_to_orm(user)
            )
        except SQLAlchemyError:
            raise UnknownUserException()

    def update_user(self, user: User) -> None:
        user_to_upd: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user.id)
        ).first()

        if user_to_upd is None:
            raise UserNotExistsException(user.id)

        user_to_upd.full_name = user.full_name

    def get_user(self, user_id: str) -> User:
        user_to_get: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user_id)
        ).first()

        if user_to_get is None:
            raise UserNotExistsException(user_id)

        return map_user_orm_to_model(user_to_get)

    def delete_user(self, user_id: str) -> None:
        user_to_del: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user_id)
        ).first()

        if user_to_del is None:
            raise UserNotExistsException(user_id)

        self._session.delete(user_to_del)
