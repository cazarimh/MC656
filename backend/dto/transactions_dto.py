from datetime import date

from pydantic import BaseModel


class TransactionRegisterResponse(BaseModel):
    transaction_id: int
    transaction_date: date
    transaction_value: float
    transaction_type: str
    transaction_category: str
    transaction_description: str | None


class TransactionsListResponse(BaseModel):
    transaction_id: int
    transaction_date: date
    transaction_value: float
    transaction_type: str
    transaction_category: str
    transaction_description: str | None
