from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    date: str
    value: float
    type: str
    category: str
    description: str | None = None

class TransactionResponse(BaseModel):
    user_id: int
    transaction_id: int
    transaction_date: date
    transaction_value: float
    transaction_type: str
    transaction_category: str
    transaction_description: str | None = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    user_hashed_password: str
    user_transactions: list[TransactionResponse] = []

    class Config:
        orm_mode = True