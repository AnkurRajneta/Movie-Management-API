from pydantic import BaseModel, EmailStr

class AuthSchema(BaseModel):
    username: str
    password: str

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class RegisterOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Use orm_mode=True if Pydantic v1
