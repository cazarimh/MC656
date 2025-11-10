from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    user_id: int


class UserResponse(BaseModel):
    id: int
    email: str


class UserRegisterResponse(BaseModel):
    message: str | None
    user: UserResponse
