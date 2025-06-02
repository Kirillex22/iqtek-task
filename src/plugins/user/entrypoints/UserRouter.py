from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_uow, get_user_service
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.User import User
from src.plugins.user.services.UserService import UserService
from src.common.exceptions.UserServiceExceptions import (
    UserAlreadyExistsException,
    UserNotExistsException, EntityValidationException
)
from src.plugins.user.views.UpdateUserView import UpdateUserView
from src.plugins.user.views.CreateUserView import CreateUserView
from src.plugins.user.views.Mappers import map_create_user_view_to_dto, \
    map_update_user_view_to_dto, map_user_model_to_user_view
from src.plugins.user.views.UserView import UserView

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=UserView)
def create_user(
        create_model: CreateUserView,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        dto_to_create = map_create_user_view_to_dto(create_model)
        user: User = service.create_user(dto_to_create, uow)
        return map_user_model_to_user_view(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except EntityValidationException as e:
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
def update_user(
        user_id: UUID,
        user: UpdateUserView,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        dto = map_update_user_view_to_dto(user_id, user)
        user: User = service.update_user(user_id, dto, uow)
        return map_user_model_to_user_view(user)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EntityValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{user_id}", status_code=201)
def delete_user(
        user_id: UUID,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        service.delete_user(user_id, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
