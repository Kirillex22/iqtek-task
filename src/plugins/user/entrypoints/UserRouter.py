from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_user_service, get_message_bus, get_uow
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.Commands import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from src.plugins.user.entities.User import User
from src.plugins.user.services import MessageBus
from src.plugins.user.services.UserService import UserService
from src.common.exceptions.UserServiceExceptions import (
    UserAlreadyExistsException,
    UserNotExistsException, InvalidUserFullNameException
)
from src.plugins.user.views.UpdateUserView import UpdateUserView
from src.plugins.user.views.CreateUserView import CreateUserView
from src.plugins.user.views.Mappers import map_user_model_to_user_view
from src.plugins.user.views.UserView import UserView

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=UserView)
async def create_user(
        create_model: CreateUserView,
        message_bus: MessageBus = Depends(get_message_bus)
):
    try:
        create_cmd = CreateUserCommand(**create_model.model_dump())
        result = (await message_bus.handle(create_cmd))[0]
        return map_user_model_to_user_view(result)

    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidUserFullNameException as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/{user_id}", response_model=UserView)
def get_user(
        user_id: UUID,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        user: User = service.get_user(user_id, uow)
        return map_user_model_to_user_view(user)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.put("/", response_model=UserView)
async def update_user(
        user_id: UUID,
        user: UpdateUserView,
        message_bus: MessageBus = Depends(get_message_bus)
):
    try:
        update_cmd = UpdateUserCommand(id=user_id, **user.model_dump())
        result = (await message_bus.handle(update_cmd))[0]
        return map_user_model_to_user_view(result)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidUserFullNameException as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{user_id}", status_code=201)
async def delete_user(
        user_id: UUID,
        message_bus: MessageBus = Depends(get_message_bus)
):
    try:
        delete_cmd = DeleteUserCommand(id=user_id)
        await message_bus.handle(delete_cmd)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
