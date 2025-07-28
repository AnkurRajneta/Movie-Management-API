from app.repository.user_repository import User_Repository
from app.schema.auth_schema import RegisterSchema, RegisterOut

class Auth_Services:
    def __init__(self, db):
        self.repo = User_Repository(db)
    
    def auth_service(self, username, password):
        user = self.repo.get_by_username(username)
        if user and user.password == password:  # Hash+check in prod
            return user
        return None

    def register_auth(self, payload: RegisterSchema):
        new_user = self.repo.create(payload)
        return RegisterOut.model_validate(new_user)
