import uuid
from uuid import UUID

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.common.exceptions.UserServiceExceptions import UserNotExistsException
from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.Mappers import map_create_user_dto_to_user
from src.plugins.user.dto.UpdateUserDTO import UpdateUserDTO
from src.plugins.user.entities.User import User
from src.plugins.user.services.tools.UserServiceExceptionHandler import UserServiceExceptionHandler, uow_wrapper

class UserService:
    def __init__(self, exception_handler = UserServiceExceptionHandler()):
        self.exception_handler = exception_handler

    @uow_wrapper
    def create_user(self, create_model: CreateUserDTO, uow: BaseUnitOfWork) -> User:
        with uow:
            user_id = uuid.uuid4()
            user = map_create_user_dto_to_user(user_id, create_model)
            created_user = uow.user_repository.create_user(user)
            user.commit_register()
        return created_user

    @uow_wrapper
    def update_user(self, user_id: UUID, data_to_update: UpdateUserDTO, uow: BaseUnitOfWork) -> User:
        with uow:
            target = uow.user_repository.get_user(user_id)
            if target is None:
                raise UserNotExistsException(user_id)

            new_full_name = data_to_update.full_name
            target.full_name = new_full_name

            updated_user = uow.user_repository.update_user(target)
        return updated_user

    @uow_wrapper
    def get_user(self, user_id: UUID, uow: BaseUnitOfWork) -> User:
        with uow:
            fetched_user = uow.user_repository.get_user(user_id)
            if fetched_user is None:
                raise UserNotExistsException(user_id)
        return fetched_user

    @uow_wrapper
    def delete_user(self, user_id: UUID, uow: BaseUnitOfWork) -> None:
        with uow:
            target = uow.user_repository.get_user(user_id)
            if target is None:
                raise UserNotExistsException(user_id)
            target.commit_delete()
            uow.user_repository.delete_user(target)
