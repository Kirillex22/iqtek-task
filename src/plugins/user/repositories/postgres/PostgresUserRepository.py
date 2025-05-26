from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.common.base.BaseUserRepository import BaseUserRepository
from src.plugins.user.dto.GetUserDTO import GetUserDTO
from src.plugins.user.entities.User import User
from src.plugins.user.repositories.postgres.Mappers import map_user_model_to_orm, map_user_orm_to_model
from src.plugins.user.repositories.postgres.orm.UserORM import UserORM
from src.common.exceptions.UserServiceExceptions import UserNotExistsException, UnknownUserException


class PostgresUserRepository(BaseUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def create_user(self, user: User) -> User:
        try:
            user_orm = map_user_model_to_orm(user)
            self._session.add(
                user_orm
            )
            self._session.flush()
            return map_user_orm_to_model(user_orm)
        except SQLAlchemyError:
            raise UnknownUserException()

    def update_user(self, user: User) -> User:
        user_to_upd: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user.id)
        ).first()

        if user_to_upd is None:
            raise UserNotExistsException(user.id)

        user_to_upd.full_name = user.full_name
        self._session.flush()
        return map_user_orm_to_model(user_to_upd)

    def get_user(self, get_model: GetUserDTO) -> User:
        user_id = get_model.id
        user_to_get: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user_id)
        ).first()

        if user_to_get is None:
            raise UserNotExistsException(user_id)

        return map_user_orm_to_model(user_to_get)

    def delete_user(self, get_model: GetUserDTO) -> None:
        user_id = get_model.id
        user_to_del: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user_id)
        ).first()

        if user_to_del is None:
            raise UserNotExistsException(user_id)

        self._session.delete(user_to_del)
