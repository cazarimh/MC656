from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    category: str
    date: str
    value: float
