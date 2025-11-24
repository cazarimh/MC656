from pydantic import BaseModel

class FinancialData(BaseModel):
    totalIncome: float
    totalExpense: float
    currentBalance: float

class GoalByType(BaseModel):
    goal_type: str
    goal_value: float

class TransactionByCategory(BaseModel):
    transaction_category: str
    transaction_value: float

class UserInfoResponse(BaseModel):
    financialData: FinancialData
    generalGoals: list[GoalByType]
    incomeList: list[TransactionByCategory]
    expenseList: list[TransactionByCategory]


class GoalInfoResponse(BaseModel):
    goal_id: int
    goal_value: float
    goal_progress: float
    goal_type: str
    goal_category: str


class TransactionByMonth(BaseModel):
    transaction_month: str
    month_income: float
    month_expense: float

class TransactionInfoResponse(BaseModel):
    lastYearTransactions: list[TransactionByMonth]
    incomeList: list[TransactionByCategory]
    expenseList: list[TransactionByCategory]