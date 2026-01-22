import jwt

from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from app.crud.users import get_user_by_id
from app.exceptions import HTTPExceptionInvalidToken
from app.models.user import User

from jwt import InvalidTokenError

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer("/auth/login")

def generate_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return access_token

def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(
            jwt=access_token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        user = get_user_by_id(user_id)
        return user
    except InvalidTokenError:
        raise HTTPExceptionInvalidToken