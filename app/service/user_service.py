from fastapi import HTTPException, status
from pydantic import model_validator
from app.repository.user_repository import User_Repository
from app.schema.user_schema import UserOut, user_create, user_update
# from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



class User_Service:
    def __init__(self, db:AsyncSession):
        self.repo = User_Repository(db)

  

    async def create_user(self, structure:user_create)->UserOut:
        new_user = await self.repo.create(structure)
        return  new_user
    
    async def getting_user(self, user_id:int):
        user =  await self.repo.get_user_id(user_id)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
        
        print(user.id)
        return  user
    
    async def getting_all(self):
        return await self.repo.get_all_user()
    
    # def getting_email(self, email:str):
    #     return self.repo.get_by_email(email)
    
    async def update_user(self, user_id:int, structure:user_update):
        return await  self.repo.update(user_id, structure)
    
    async def delete_user(self, user_id:int):
        return await  self.repo.delete(user_id)

