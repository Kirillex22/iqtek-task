from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from domain.base.BaseUserRepository import BaseUserRepository
from domain.entities.User import User
from repositories.postgres.Mappers import map_user_model_to_orm
from repositories.postgres.orm.UserORM import UserORM
from shared.exceptions.UserServiceExceptions import UserNotExistsException, UserAlreadyExistsException, \
    UnknownUserException


class PostgresUserRepository(BaseUserRepository):
    def __init__(self, session: Session):
        self._session = session

    async def create_user(self, user: User) -> None:
        try:
            self._session.add(
                map_user_model_to_orm(user)
            )
        except IntegrityError:
            raise UserAlreadyExistsException(user)
        except SQLAlchemyError:
            raise UnknownUserException()

    async def update_user(self, user: User) -> None:
        user_to_upd: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user.id)
        ).first()

        if user_to_upd is None:
            raise UserNotExistsException(user.id)

        user_to_upd.full_name = user.full_name

    async def get_user(self, user_id: str) -> Optional[User]:
        user_to_get: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user_id)
        ).first()

        return user_to_get

    async def delete_user(self, user_id: str) -> None:
        user_to_del: UserORM = self._session.exec(
            select(UserORM).where(UserORM.id == user_id)
        ).first()

        if user_to_del is None:
            raise UserNotExistsException(user_id)

        self._session.delete(user_to_del)
