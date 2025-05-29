import uuid
from functools import wraps
from typing import Callable, Optional
from uuid import UUID

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.common.exceptions.UserServiceExceptions import UserNotExistsException
from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.Mappers import map_user_dto_to_user, map_create_user_dto_to_user
from src.plugins.user.dto.UpdateUserDTO import UpdateUserDTO
from src.plugins.user.dto.UserDTO import UserDTO
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
    def create_user(self, create_model: CreateUserDTO, uow: BaseUnitOfWork) -> UserDTO:
        with uow:
            user_id = uuid.uuid4()
            user = map_create_user_dto_to_user(user_id, create_model)
            created_user = uow.user_repository.create_user(user)
        return created_user

    @uow_wrapper
    def update_user(self, user_id: UUID, data_to_update: UpdateUserDTO, uow: BaseUnitOfWork) -> UserDTO:
        with uow:
            target_dto = uow.user_repository.get_user(user_id)
            if target_dto is None:
                raise UserNotExistsException(user_id)
            target = map_user_dto_to_user(target_dto)
            target.full_name = data_to_update.full_name
            updated_user = uow.user_repository.update_user(target)
        return updated_user

    @uow_wrapper
    def get_user(self, user_id: UUID, uow: BaseUnitOfWork) -> UserDTO:
        with uow:
            fetched_user = uow.user_repository.get_user(user_id)
            if fetched_user is None:
                raise UserNotExistsException(user_id)
        return fetched_user

    @uow_wrapper
    def delete_user(self, user_id: UUID, uow: BaseUnitOfWork) -> None:
        with uow:
            target_dto = uow.user_repository.get_user(user_id)
            if target_dto is None:
                raise UserNotExistsException(user_id)
            target = map_user_dto_to_user(target_dto)
            uow.user_repository.delete_user(target)
