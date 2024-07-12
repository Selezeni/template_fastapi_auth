from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.user_models import BaseUser, Token, UserDTO
from utils.auth import AuthService, get_current_user

router = APIRouter(
    prefix="/auth/token",
    tags=["Авторизация"],
)


@router.post(
    "",
)
async def login(
    user: BaseUser = Depends(OAuth2PasswordRequestForm),
    service: AuthService = Depends(),
) -> Token:
    return await service.authenticate_user(user)


@router.get("/user")
async def get_info(current_user: UserDTO = Depends(get_current_user)) -> UserDTO:
    return current_user
