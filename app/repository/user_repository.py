from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import UserModel
from app.schema.user_schema import user_update

class User_Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_all_user(self):
        return self.db.query(UserModel).all()

    def create(self, structure) -> UserModel:
        user = UserModel(
            username=structure.username,
            email=structure.email,
            password=structure.password  # ⚠️ hash in real apps
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, id: int, structure: user_update):
        user = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            return None  # Optional: raise 404
        user.username = structure.username
        user.email = structure.email
        user.password = structure.password
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, id: int):
        user = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            return False  # Optional: raise 404
        self.db.delete(user)
        self.db.commit()
        return True
