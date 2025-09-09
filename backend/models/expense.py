from pydantic import BaseModel

class Expense(BaseModel):
    id: int
    user_id: int
    category: str
    date: str
    value: float