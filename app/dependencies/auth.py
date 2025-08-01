from fastapi import Header, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.repository.user_repository import User_Repository
from app.core.jwt import decode_jwt

def get_current_user(
    request:Request,
    db: Session = Depends(get_db)
):
    authorization = request.headers.get('Authorization')

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    token = authorization[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empty token in Authorization header"
        )

    try:
        payload = decode_jwt(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}"
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject (sub) claim"
        )

    try:
        user = User_Repository(db).get_by_username(username)
    except Exception as db_exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error while accessing user data"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
