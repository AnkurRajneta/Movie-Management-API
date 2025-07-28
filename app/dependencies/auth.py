from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.repository.user_repository import User_Repository
from app.core.jwt import decode_jwt

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    print(f"Authorization header received: {authorization}")
    if not authorization or not authorization.lower().startswith("bearer "):
        print("Invalid or missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = authorization[7:].strip()
    print(f"Extracted token: {token}")
    try:
        payload = decode_jwt(token)
        print(f"Decoded JWT payload: {payload}")
    except Exception as e:
        print(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}"
        )

    username = payload.get("sub")
    if not username:
        print("JWT token has no subject claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim"
        )
    user = User_Repository(db).get_by_username(username)
    if not user:
        print(f"User not found in database: {username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    print(f"Authenticated user: {username}")
    return user

