from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

class ErrorUserAlreadyExists(BaseModel):
    detail: str = "User already exists"

class ErrorIncorrectUsernameOrPassword(BaseModel):
    detail: str = "Incorrect username or password"

class ErrorInvalidToken(BaseModel):
    detail: str = "Invalid token"