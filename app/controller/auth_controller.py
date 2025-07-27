from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.controller.movie_controller import *
from app.controller.user_controller import create_user, get_user, getting_all
from app.controller.auth_controller import *
from app.models.user_model import UserModel
from app.schema.auth_schema import AuthSchema, RegisterSchema
from app.service import auth_service
from app.service.auth_service import Auth_Services

router = APIRouter()



@router.post('/login')
def login(payload:AuthSchema, db:Session = Depends(get_db)):
    service  = Auth_Services(db)
    user = service.auth_service(payload.username, payload.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect details")
    
    return {"messsage": "Logged in successfully"}

@router.post('/Register')
def register(payload:RegisterSchema, db:Session = Depends(get_db)):
    service = Auth_Services(db)
    register_user = service.register_auth(payload)


    