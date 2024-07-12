from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_models import UserCreate
from repositories.user_repository import UserRepository


class UserService():
    
    repository = UserRepository()
    
    async def create_user(self, user: UserCreate, session: AsyncSession):
        return await self.repository.create_new_user(user, session)
    
    async def update_user(self, id: int, user_data: UserCreate, session: AsyncSession):
        return await self.repository.update_user_by_id(id, user_data, session)
    
    async def get_user(self, id: int, name: str, session: AsyncSession):
        return await self.repository.get_by_id_name(id, name, session)
    
    async def delete(self, id: int, session: AsyncSession):
        return await self.repository.delete_by_id(id, session)
    