from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

class ExpenseCreate(BaseModel):
    category: str
    date: str
    value: float

class Expense(BaseModel):
    id: int
    user_id: int
    category: str
    date: str
    value: float