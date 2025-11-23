from sqlalchemy.orm import Session
from database.models import Transaction

def compute_current_value(db, user_id, goal_model):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == goal_model.goal_type,
        Transaction.transaction_category == goal_model.goal_category
    ).all()

    total = sum(t.transaction_value for t in transactions)
    return total
