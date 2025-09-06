from datetime import datetime

from pydantic import BaseModel


class Expense(BaseModel):
    id: int
    user_id: int
    title: str
    amount: float
    category: str | None
    date: datetime
    description: str | None
