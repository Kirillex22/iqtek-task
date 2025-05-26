from functools import wraps
from typing import Callable, Optional

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.User import User
from src.plugins.user.services.tools.UserServiceExceptionHandler import UserServiceExceptionHandler


def uow_wrapper(func) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Optional:
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            self.exception_handler.handle(e)
            return None

    return wrapper


class UserService:
    def __init__(self):
        self.exception_handler = UserServiceExceptionHandler()

    @uow_wrapper
    def create_user(self, user: User, uow: BaseUnitOfWork) -> None:
        with uow:
            return uow.user_repository.create_user(user)

    @uow_wrapper
    def update_user(self, user: User, uow: BaseUnitOfWork) -> None:
        with uow:
            uow.user_repository.update_user(user)

    @uow_wrapper
    def get_user(self, user_id: str, uow: BaseUnitOfWork) -> User:
        with uow:
            user = uow.user_repository.get_user(user_id)
        return user

    @uow_wrapper
    def delete_user(self, user_id: str, uow: BaseUnitOfWork) -> None:
        with uow:
            uow.user_repository.delete_user(user_id)
