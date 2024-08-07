from enum import Enum

from pydantic import BaseModel, Field


class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class BaseUser(BaseModel):
    username: str = Field(pattern=r"^[a-zA-Z0-9_-]{3,16}$")
    password: str = Field(min_length=8)

    class Config:
        extra = "ignore"
        from_atributes = True


class UserDTO(BaseModel):
    id: int
    sub: str
    role: str
    is_active: bool


class UserCreate(BaseUser):
    role: UserRoleEnum = Field(default=None)
    is_active: bool = Field(default=None)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
