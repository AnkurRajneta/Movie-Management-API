from datetime import datetime
from token import OP
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import DateTime


class user_create(BaseModel):
    username : str = Field(min_length=3, max_length=50, example="Ankur Rajneta")
    email : EmailStr = Field(example="ankurrajneta@gmail.com")
    password : str = Field(min_length=5, example="strongpassword")

class user_update(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email:Optional[EmailStr] = Field(None)
    password:Optional[str] = Field(None, min_length=5)
    

class UserOut(BaseModel):
     id:int
     username: str
     email: EmailStr
     created_at:datetime
     updated_at:datetime
        
        
     class config:
        from_attributes=True