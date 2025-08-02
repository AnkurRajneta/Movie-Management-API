from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import UserModel
from app.schema.user_schema import user_update

class User_Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_id(self, user_id: int):
        stmt = select(UserModel).where(UserModel.id == user_id)
        execute = await self.db.execute(stmt)
        return execute.scalars().first()

    async def get_by_username(self, username: str):
        user = select(UserModel).where(UserModel.username == username)
        result = await self.db.execute(user)
        return result.scalars().first()
    
    async def get_all_user(self):
        user_all = select(UserModel)
        result = await self.db.execute(user_all)
        return result.scalars().all()

    async def create(self, structure) -> UserModel:
        user = UserModel(
            username=structure.username,
            email=structure.email,
            password=structure.password  # ⚠️ hash in real apps
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update(self, id: int, structure: user_update):
        user_stmt = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(user_stmt)
        updated = result.scalars().first()
        if not updated:
            return None
        updated.username = structure.username
        updated.email = structure.email
        updated.password = structure.password
        await self.db.commit()
        await self.db.refresh(updated)
        return updated
    
    async def delete(self, id: int):
        user_stmt = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(user_stmt)
        user = result.scalars().first()
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True
