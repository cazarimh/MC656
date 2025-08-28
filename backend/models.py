from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: int
    email: str