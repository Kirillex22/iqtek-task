from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_uow
from domain.base.BaseUnitOfWork import BaseUnitOfWork
from domain.entities.User import User
from domain.services.UserService import UserService
from shared.exceptions.UserServiceExceptions import (
    UserAlreadyExistsException,
    UserNotExistsException
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user: User,
        uow: BaseUnitOfWork = Depends(get_uow),
):
    service = UserService()
    try:
        await service.create_user(user, uow)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: str,
        uow: BaseUnitOfWork = Depends(get_uow),
):
    service = UserService()
    try:
        return await service.get_user(user_id, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.put("/", response_model=None)
async def update_user(
        user: User,
        uow: BaseUnitOfWork = Depends(get_uow),
):
    service = UserService()
    try:
        await service.update_user(user, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete("/{user_id}", status_code=204)
async def delete_user(
        user_id: str,
        uow: BaseUnitOfWork = Depends(get_uow),
):
    service = UserService()
    try:
        await service.delete_user(user_id, uow)
    except UserNotExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
