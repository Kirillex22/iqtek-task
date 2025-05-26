from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_uow, get_user_service
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.User import User
from src.plugins.user.services.UserService import UserService
from src.common.exceptions.UserServiceExceptions import (
    UserAlreadyExistsException,
    UserNotExistsException
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
        user: User,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        service.create_user(user, uow)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))


@user_router.get("/{user_id}", response_model=User)
def get_user(
        user_id: str,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        return service.get_user(user_id, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.put("/", response_model=None)
def update_user(
        user: User,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        service.update_user(user, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete("/{user_id}", status_code=204)
def delete_user(
        user_id: str,
        uow: BaseUnitOfWork = Depends(get_uow),
        service: UserService = Depends(get_user_service)
):
    try:
        service.delete_user(user_id, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
