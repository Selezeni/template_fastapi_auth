from abc import ABC, abstractmethod

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from models.models import UserModelOrm
from models.user_models import UserCreate, UserDTO
from utils.auth import AuthService
from utils.exceptions import WrongUserNameOrPasswordError


class AbstractRepository(ABC):
    @abstractmethod    
    def create_new_user(self,):
        pass
    
    @abstractmethod
    def update_user_by_id(self):
        pass
    
    @abstractmethod
    def get_by_id_name(self):
        pass
    
    @abstractmethod
    def delete_by_id(self):
        pass
    
    
class UserRepository(AbstractRepository):
        
    async def create_new_user(self, user: UserCreate, session: AsyncSession):
        try:
            stmt = UserModelOrm(
                username=user.username,
                hashed_password=await AuthService().hash_password(user.password),
            )
            session.add(stmt)
            await session.commit()
        except Exception as e:
            print(e)
            raise
        return {"message": f"user with id={stmt.id} created"}

    async def update_user_by_id(self, id: int, user_data: UserCreate, session: AsyncSession):
        try:
            query = select(UserModelOrm).where(UserModelOrm.id == id)
            result = await session.execute(query)
            user_from_db = result.scalar_one_or_none()
        except Exception as e:
            print(e)
            raise
        
        if not user_from_db:
            raise WrongUserNameOrPasswordError()
        
        user_from_db.username = user_data.username
        user_from_db.hashed_password = await AuthService().hash_password(user_data.password)
        user_from_db.role = user_data.role
        user_from_db.is_active = user_data.is_active
        session.add(user_from_db)
        await session.commit()
        
        return {"message": f"user with id={id} updated"}
        
    async def get_by_id_name(self, id: int, name: str, session: AsyncSession):
        try:
            query = select(UserModelOrm).filter(
                UserModelOrm.id == id, UserModelOrm.username == name
            )
            result = await session.execute(query)
            user_from_db = result.scalar_one()
            user_out = UserDTO(
                id=user_from_db.id,
                sub=user_from_db.username,
                role=user_from_db.role,
                is_active=user_from_db.is_active
            )
        except NoResultFound as e:
            print(e)
            raise WrongUserNameOrPasswordError()
        return user_out

    async def delete_by_id(self, id: int, session: AsyncSession):
        try:
            stmt = delete(UserModelOrm).where(UserModelOrm.id == id)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(e)
            raise
        return {"message": f"user with id={id} deleted"}