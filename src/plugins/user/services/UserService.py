from functools import wraps
from typing import Callable, Optional

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.GetUserDTO import GetUserDTO
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
    def create_user(self, create_model: CreateUserDTO, uow: BaseUnitOfWork) -> User:
        user = User(full_name=create_model.full_name)
        with uow:
            created_user = uow.user_repository.create_user(user)
        return created_user

    @uow_wrapper
    def update_user(self, user: User, uow: BaseUnitOfWork) -> User:
        with uow:
            updated_user = uow.user_repository.update_user(user)
        return updated_user

    @uow_wrapper
    def get_user(self, get_model: GetUserDTO, uow: BaseUnitOfWork) -> User:
        with uow:
            user = uow.user_repository.get_user(get_model)
        return user

    @uow_wrapper
    def delete_user(self, get_model: GetUserDTO, uow: BaseUnitOfWork) -> None:
        with uow:
            uow.user_repository.delete_user(get_model)
