from app.repository.user_repository import User_Repository
from app.schema.auth_schema import RegisterSchema, RegisterOut
from sqlalchemy.ext.asyncio import AsyncSession

class Auth_Services:
    def __init__(self, db: AsyncSession):
        self.repo = User_Repository(db)
    
    async def auth_service(self, username, password):
        user = await self.repo.get_by_username(username)
        if user and user.password == password:  
            return user
        return None

    async def register_auth(self, payload: RegisterSchema):
        new_user = await self.repo.create(payload)
        return RegisterOut.model_validate(new_user)
