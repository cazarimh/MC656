from app.models.expenseModel import Expense
from app.services.expenseService import ExpenseService
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/expenses", tags=["expenses"])

expenseService = ExpenseService()


@router.get("/user/{userId}", response_model=list[Expense])
async def getUserExpense(userId: int):
    try:
        # TODO: add validation: user exists | depends: userService.userExists()
        expenses = await expenseService.getExpenseByUserId(userId)
        return expenses

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch expenses data",
        )
