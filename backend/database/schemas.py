from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    general_id = 0

    id: int
    name: str
    email: str
    hashed_password: str

    def __init__(self):
        User.general_id += 1
        self.id = User.general_id

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    date: str
    value: float
    type: str
    category: str
    description: str

class Transaction(BaseModel):
    general_id = 0

    user_id: int
    id: int
    date: date
    value: float
    type: str
    category: str
    description: str

    def __init__(self):
        Transaction.general_id += 1
        self.id = Transaction.general_id

    class Config:
        orm_mode = True