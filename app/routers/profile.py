from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.utils.jwt import get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.schemas.errors import ErrorInvalidToken

profile_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorInvalidToken,
            "headers": {
                "WWW-Authenticate": {
                    "schema": {"type": "string", "example": "Bearer"}
                }
            }
        }
    }
)

@profile_router.get("/me", response_model=UserRead)
def get_me(user: Annotated[UserRead, Depends(get_current_user)]):
    return user