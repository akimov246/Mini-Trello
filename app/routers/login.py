from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.crud.users import get_user_by_username
from app.exceptions import HTTPExceptionIncorrectUsernameOrPassword
from app.utils.password import verify_password
from app.utils.jwt import generate_access_token
from app.schemas.token import Token
from app.schemas.errors import ErrorIncorrectUsernameOrPassword

login_router = APIRouter(
    prefix="/auth",
    tags=["users"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorIncorrectUsernameOrPassword,
            "headers": {
                "WWW-Authenticate": {
                    "schema": {"type": "string", "example": "Bearer"}
                }
            }
        },
        status.HTTP_200_OK: {
            "model": Token
        }
    }
)

@login_router.post("/login", response_model=Token)
def login_user(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_by_username(credentials.username)
    if not user:
        raise HTTPExceptionIncorrectUsernameOrPassword
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPExceptionIncorrectUsernameOrPassword
    access_token = generate_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")