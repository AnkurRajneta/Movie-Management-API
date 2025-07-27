from email.policy import HTTP


from click import Option
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from app.schema.user_schema import  UserOut, user_create, user_update
from app.models.user_model import UserModel
from sqlalchemy.orm import Session
from app.core.security import hash_password 
from typing import Optional


class User_Repository:
    def __init__(self, db:Session):
        self.db = db


    def get_user(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()


    def get_all_user(self):
        return self.db.query(UserModel).all()
  
    
    def get_by_email(self, email:str):
        return self.db.query(UserModel).filter(email == UserModel.email).first()
    

    def create(self,structure:user_create) -> UserOut:
        user = UserModel(username= structure.username, email = structure.email, password = structure.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id:int, structure:user_update):
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if structure.email is not None:
            user.email = structure.email

        if structure.username is not None:
            user.username = structure.username

        if structure.password is not None:
            user.password = hash_password(structure.password)

        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self,user_id: int):
        user =  self.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found to delete")

        self.db.delete(user)
        self.db.commit()
