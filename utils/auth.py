import datetime
import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from models.models import UserModelOrm
from models.user_models import BaseUser, Token, UserCreate, UserDTO, UserRoleEnum
from utils.exceptions import (
    BadCredentialsError,
    InactiveUserError,
    UserAlreadyExistsError,
    WrongUserNameOrPasswordError,
)

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDTO:
    return await AuthService.validate_token(token=token)


class AuthService:
    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    async def validate_token(cls, token: str) -> UserDTO:
        try:
            payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        except PyJWTError:
            raise BadCredentialsError()
        user_data = {
            "id": payload.get("id"),
            "sub": payload.get("sub"),
            "role": payload.get("role"),
            "is_active": payload.get("is_active"),
        }
        try:
            current_user = UserDTO(**user_data)
        except ValidationError as e:
            print(e)
            raise BadCredentialsError()
        return current_user

    @classmethod
    async def create_token(cls, user: UserDTO) -> Token:
        now = datetime.datetime.now()
        payload = {
            "iat": now,
            "exp": now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "id": user.id,
            "sub": user.sub,
            "role": user.role,
            "is_active": user.is_active,
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

        return Token(access_token=token)

    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        self.session = session

    async def register_new_user(self, user_data: UserCreate):
        try:
            stmt = UserModelOrm(
                username=user_data.username,
                hashed_password=await self.hash_password(user_data.password),
                role=user_data.role,
            )
            self.session.add(stmt)
            await self.session.commit()
        except IntegrityError as e:
            print(e)
            raise UserAlreadyExistsError()

        return {"status": f"{status.HTTP_201_CREATED} CREATED"}

    async def authenticate_user(self, user: BaseUser) -> Token:
        try:
            query = select(UserModelOrm).filter(UserModelOrm.username == user.username)
            result = await self.session.execute(query)
            user_from_db = result.scalar()
        except Exception as e:
            print(e)
            raise
        if not user_from_db:
            raise WrongUserNameOrPasswordError()

        elif not await self.verify_password(
            user.password, user_from_db.hashed_password
        ):
            raise WrongUserNameOrPasswordError()

        elif not user_from_db.is_active:
            raise InactiveUserError()

        try:
            token: Token = await self.create_token(
                UserDTO(
                    id=user_from_db.id,
                    sub=user_from_db.username,
                    role=UserRoleEnum(user_from_db.role),
                    is_active=user_from_db.is_active,
                )
            )
        except ValidationError as e:
            print(e)
            raise

        return token
