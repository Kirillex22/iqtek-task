from typing import Callable, Optional

from domain.base.BaseUnitOfWork import BaseUnitOfWork
from domain.entities.User import User
from domain.services.tools.UserServiceExceptionHandler import UserServiceExceptionHandler
from shared.exceptions.UserServiceExceptions import UserNotExistsException


class UserService:
    def __init__(self):
        self.exception_handler = UserServiceExceptionHandler()

    async def _uow_wrapper(self, uow: BaseUnitOfWork, action: Callable) -> Optional[User]:
        try:
            async with uow:
                result = await action()
                return result

        except Exception as e:
            self.exception_handler.handle(e)

    async def create_user(self, user: User, uow: BaseUnitOfWork) -> None:
        await self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.create_user(user)
        )

    async def update_user(self, user: User, uow: BaseUnitOfWork) -> None:
        await self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.update_user(user)
        )

    async def get_user(self, user_id: str, uow: BaseUnitOfWork) -> User:
        user = await self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.get_user(user_id)
        )

        if user is None:
            raise UserNotExistsException(user_id=user_id)

        return user

    async def delete_user(self, user_id: str, uow: BaseUnitOfWork) -> None:
        await self._uow_wrapper(
            uow=uow,
            action=lambda: uow.user_repository.delete_user(user_id)
        )
