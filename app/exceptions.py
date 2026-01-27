from fastapi import HTTPException, status

HTTPExceptionUserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

HTTPExceptionIncorrectUsernameOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPExceptionInvalidToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)

class BoardNotFoundError(Exception):
    pass

class ListNotFoundError(Exception):
    pass

class ListInvalidNewPositionError(Exception):
    pass