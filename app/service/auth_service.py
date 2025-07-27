
import re
from sqlalchemy import all_
from sqlalchemy.orm import Session
from app.models.user_model import UserModel
from app.repository.user_repository import User_Repository
from app.schema.auth_schema import AuthSchema, RegisterSchema, RegisterOut


class Auth_Services:
    def __init__(self, db: Session):
        self.repo = User_Repository(db)
    
    def auth_service(self, username, password):
        all_user = self.repo.get_all_user()
        for user in all_user:
            if user.username ==username:
                if user.password == password:
                    return user

        return None      

    def register_auth(self, payload:RegisterSchema):
        new_user = self.repo.create(payload)
        return RegisterOut.model_validate(new_user)

        
        