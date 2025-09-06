from app.models.expenseModel import Expense
from app.services.expenseService import ExpenseService
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/expenses", tags=["expenses"])

expenseService = ExpenseService()


@router.get("/user/{userId}", response_model=list[Expense])
async def getUserExpense(userId: int):  
    try:
        # TODO: add validation: user exists | depends: userService.userExists()

        from app.main import dict_db
        
        # Validação: verifica se o usuário existe
        if userId not in dict_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        expenses = await expenseService.getExpenseByUserId(userId)
        return expenses
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch expenses data",
        )
