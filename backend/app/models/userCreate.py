from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str