from ctypes import Structure
import email
from tempfile import template
from typing import List

from fastapi.responses import HTMLResponse
from h11 import Request
from pydantic import EmailStr
from app.service.user_service import User_Service
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.schema.user_schema import user_create, user_update, UserOut
from fastapi import APIRouter, Depends


router = APIRouter()

    

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id:int, db: Session = Depends(get_db)):
    service = User_Service(db)
    return service.getting_user(user_id)

@router.get("", response_model=List[UserOut])
def getting_all(db:Session = Depends(get_db)):
    service = User_Service(db)
    return service.getting_all()

# @router.get('/email/{email}', response_model=UserOut) 
# def get_by_email(email: EmailStr, db: Session = Depends(get_db)):
#     service = User_Service(db)
#     return service.getting_email(email)


@router.post('', response_model=UserOut)
def create_user(structure:user_create, db:Session = Depends(get_db)):
    service = User_Service(db)
    return service.create_user(structure)   

@router.put('/{userId}', response_model=user_update)
def update_user(structure:user_create, user_id: int, db:Session = Depends(get_db)):
    service = User_Service(db)
    return service.update_user(user_id, structure)


@router.delete('/{userId}')
def delete_user(user_id:int, db:Session = Depends(get_db)):
    service = User_Service(db)
    return service.delete_user(user_id)
