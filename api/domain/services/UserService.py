from typing import Callable, Optional

from domain.base.BaseUnitOfWork import BaseUnitOfWork
from domain.entities.User import User
from domain.services.tools.UserServiceExceptionHandler import UserServiceExceptionHandler


class UserService:
    def __init__(self):
        self.exception_handler = UserServiceExceptionHandler()

    def _uow_wrapper(self, uow: BaseUnitOfWork, action: Callable) -> Optional[User]:
        try:
            with uow:
                result = action()

            return result

        except Exception as e:
            self.exception_handler.handle(e)

    def create_user(self, user: User, uow: BaseUnitOfWork) -> None:
        self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.create_user(user)
        )

    def update_user(self, user: User, uow: BaseUnitOfWork) -> None:
        self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.update_user(user)
        )

    def get_user(self, user_id: str, uow: BaseUnitOfWork) -> User:
        user = self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.get_user(user_id)
        )

        return user

    def delete_user(self, user_id: str, uow: BaseUnitOfWork) -> None:
        self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.delete_user(user_id)
        )
