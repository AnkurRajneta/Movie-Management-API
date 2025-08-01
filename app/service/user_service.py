from fastapi import HTTPException, status
from pydantic import model_validator
from app.repository.user_repository import User_Repository
from app.schema.user_schema import UserOut, user_create, user_update
from sqlalchemy.orm import Session



class User_Service:
    def __init__(self, db:Session):
        self.repo = User_Repository(db)

  

    def create_user(self, structure:user_create)->UserOut:
        new_user = self.repo.create(structure)
        return new_user
    
    def getting_user(self, user_id:int):
        user =  self.repo.get_user_id(user_id)
        print(user.id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
        return user
    
    def getting_all(self):
        return self.repo.get_all_user()
    
    # def getting_email(self, email:str):
    #     return self.repo.get_by_email(email)
    
    def update_user(self, user_id:int, structure:user_update):
        return self.repo.update(user_id, structure)
    
    def delete_user(self, user_id:int):
        return self.repo.delete(user_id)

