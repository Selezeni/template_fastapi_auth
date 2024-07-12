from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from models.user_models import BaseUser, UserCreate, UserDTO, UserRoleEnum
from services.user_service import UserService
from utils.auth import get_current_user
from utils.exceptions import NotEnoughRightsError
from utils.exceptions import NotEnoughRightsError

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.post("/create")
async def create_user(
    user: BaseUser,
    service: UserService = Depends(),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserDTO = Depends(get_current_user)
):
    if current_user.role != UserRoleEnum.ADMIN:
        raise NotEnoughRightsError()
    return await service.create_user(UserCreate(**user.model_dump()), session)


@router.post("/update/{id}")
async def update_user(
    id: int,
    user_data: UserCreate = Body(...),
    service: UserService = Depends(),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserDTO = Depends(get_current_user)
):
    if current_user.role != UserRoleEnum.ADMIN:
        raise NotEnoughRightsError()
    return await service.update_user(id, user_data, session)


@router.get("/get/{id}")
async def user_info_by_id(
    id: int,
    name: str,
    service: UserService = Depends(),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserDTO = Depends(get_current_user)
):
    if current_user.role != UserRoleEnum.ADMIN:
        raise NotEnoughRightsError()
    return await service.get_user(id, name, session)


@router.delete("/delete/{id}")
async def delete_user(
    id: int,
    service: UserService = Depends(),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserDTO = Depends(get_current_user)
):
    if current_user.role != UserRoleEnum.ADMIN:
        raise NotEnoughRightsError()
    return await service.delete(id, session)
