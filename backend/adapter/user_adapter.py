from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    user_id: int