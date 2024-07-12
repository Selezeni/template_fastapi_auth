from enum import Enum

from pydantic import BaseModel, Field


class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class BaseUser(BaseModel):
    username: str
    password: str

    class Config:
        extra = "ignore"
        from_atributes=True

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
