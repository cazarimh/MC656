from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import get_db
from utils.reports_utils import (
    get_monthly_summary,
    get_expenses_by_category,
    get_income_by_category
)

router = APIRouter(prefix="/reports")

router = APIRouter()

@router.get("/{user_id}/reports/monthly")
def monthly_report(user_id: int, db: Session = Depends(get_db)):
    return get_monthly_summary(db, user_id)

@router.get("/{user_id}/reports/expenses")
def expenses_report(user_id: int, db: Session = Depends(get_db)):
    return get_expenses_by_category(db, user_id)

@router.get("/{user_id}/reports/income")
def income_report(user_id: int, db: Session = Depends(get_db)):
    return get_income_by_category(db, user_id)

