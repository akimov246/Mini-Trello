from fastapi import APIRouter, status
from app.schemas.user import UserCreate, UserRead
from app.schemas.errors import ErrorUserAlreadyExists
from app.crud.users import user_exists, create_user
from app.exceptions import HTTPExceptionUserAlreadyExists

signup_router = APIRouter(
    prefix="/auth",
    tags=["users"],
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorUserAlreadyExists, "description": "User already exists"},
        status.HTTP_201_CREATED: {"model": UserRead, "description": "User created"},
    }
)

@signup_router.post('/signup', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup_user(credentials: UserCreate):
    if user_exists(credentials.username):
        raise HTTPExceptionUserAlreadyExists
    user = create_user(credentials)
    return user