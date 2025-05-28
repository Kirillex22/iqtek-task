from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.common.base.BaseUserRepository import BaseUserRepository
from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.Mappers import map_create_user_dto_to_user, map_user_to_user_dto
from src.plugins.user.dto.UserDTO import UserDTO
from src.plugins.user.entities.User import User
from src.common.exceptions.UserServiceExceptions import UnknownUserException


class PostgresUserRepository(BaseUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def create_user(self, user_data: CreateUserDTO) -> UserDTO:
        try:
            user = map_create_user_dto_to_user(user_data)
            self._session.add(user)
            self._session.flush() # todo: мб включить autoflush???
            return map_user_to_user_dto(user)
        except SQLAlchemyError:
            raise UnknownUserException()

    def update_user(self, user: User) -> UserDTO:
        self._session.merge(user)
        self._session.flush()
        return map_user_to_user_dto(user)

    def get_user(self, user_id: int) -> UserDTO | None:
        fetched_user: User | None = self._session.query(User).filter_by(id=user_id).first()
        if fetched_user is None:
            return None
        return map_user_to_user_dto(fetched_user)

    def delete_user(self, user: User) -> None:
        connected_user = self._session.merge(user)
        self._session.delete(connected_user)
