from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import UserModel

class User_Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_all_user(self):
        return self.db.query(UserModel).all()

    def create(self, structure) -> UserModel:
        user = UserModel(
            username=structure.username,
            email=structure.email,
            password=structure.password  # Hash in production!
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
