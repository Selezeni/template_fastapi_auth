from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.user_models import UserRoleEnum


class Base(DeclarativeBase):
    pass


class UserModelOrm(Base):
    __tablename__ = "api_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(
        String(10), nullable=True, default=UserRoleEnum.USER
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)
