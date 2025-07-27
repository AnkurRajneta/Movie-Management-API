from sqlalchemy.orm import Session
from app.repository.user_repository import *
from app.schema.auth_schema import AuthSchema


class Auth_Services:
    def __init__(self, db: Session):
        self.repo = User_Repository(db)
    
    def auth_schema()