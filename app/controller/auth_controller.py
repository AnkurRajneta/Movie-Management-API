from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schema.auth_schema import AuthSchema, RegisterSchema, RegisterOut
from app.service.auth_service import Auth_Services
from app.dependencies.auth import get_current_user
from app.config.database import get_db
from app.core.jwt import create_jwt
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()  # Declare security scheme for Swagger UI

@router.post('/login')
def login(payload: AuthSchema, db: Session = Depends(get_db)):
    service = Auth_Services(db)
    user = service.auth_service(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect details")
    token = create_jwt({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post('/register', response_model=RegisterOut)
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    service = Auth_Services(db)
    return service.register_auth(payload)

@router.get('/me', dependencies=[Depends(security)])
def me(current_user = Depends(get_current_user)):
    return current_user
