from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    date: str
    value: float
    category: str
    type: str
    description: str

class Transaction(BaseModel):
    user_id: int
    id: int
    date: str
    value: float
    category: str
    type: str
    description: str
    class Config:
        orm_mode = True