from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import get_db
from utils.dashboard_utils import get_dashboard_totals

router = APIRouter()

@router.get("/{user_id}/dashboard/totals")
def dashboard_totals(user_id: int, db: Session = Depends(get_db)):
    return get_dashboard_totals(db, user_id)
