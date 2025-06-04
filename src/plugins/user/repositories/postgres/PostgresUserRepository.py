from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.common.base.BaseUserRepository import BaseUserRepository
from src.plugins.user.orm.UserInDB import UserInDB
from src.plugins.user.dto.Mappers import map_user_to_db_user_dto, map_db_user_dto_to_user
from src.plugins.user.entities.User import User
from src.common.exceptions.UserServiceExceptions import UnknownUserException


class PostgresUserRepository(BaseUserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    def create_user(self, user: User) -> User:
        db_user = map_user_to_db_user_dto(user)
        try:
            self._session.add(db_user)
            self.seen.add(user)
            return user
        except SQLAlchemyError:
            raise UnknownUserException()

    def update_user(self, user: User) -> User:
        db_user = map_user_to_db_user_dto(user)
        self._session.merge(db_user)
        self._session.flush()
        user = map_db_user_dto_to_user(db_user)
        self.seen.add(user)
        return user

    def get_user(self, user_id: UUID) -> User | None:
        fetched_user: UserInDB | None = self._session.query(UserInDB).filter_by(id=user_id).first()
        if fetched_user is None:
            return None

        user = map_db_user_dto_to_user(fetched_user)
        self.seen.add(user)

        return user

    def delete_user(self, user: User) -> None:
        db_user = map_user_to_db_user_dto(user)
        connected_user = self._session.merge(db_user)
        self._session.delete(connected_user)