from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.controller.movie_controller import *
from app.controller.user_controller import create_user, get_user, getting_all
from app.controller.auth_controller import *
from app.models.user_model import UserModel
from app.schema.auth_schema import AuthSchema
from app.service.auth_service import *

router = APIRouter()


def authenticateUser(username:str, password:str):
    if(password == getting_all(UserModel.password)):
        return "Logged in successfully"

@router.post('/login')
def login(payload:AuthSchema, db:Session = Depends(get_db)):
    user = Auth_Services(payload.username, payload.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect details")
    


# @router.post('/Register')
# def register(form_data = Annotated[OAuth2PasswordBearer, Depends()]):
#     new_register = create_user()
    