from sqlalchemy.orm import Session
from database.models import Transaction

def get_dashboard_totals(db: Session, user_id: int):
    receitas = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "Receita"
    ).all()

    despesas = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "Despesa"
    ).all()

    total_receitas = sum(t.transaction_value for t in receitas)
    total_despesas = sum(t.transaction_value for t in despesas)

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": total_receitas - total_despesas
    }
