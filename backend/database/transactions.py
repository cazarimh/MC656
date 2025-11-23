from sqlalchemy.orm import Session
from datetime import datetime as dt
from database.models import Transaction
from database.schemas import TransactionCreate
from sqlalchemy import func

def create_transaction_db(db: Session, user_id: int, transaction: TransactionCreate):
    new_transaction = Transaction(user_id=user_id,
                                  transaction_date=dt.fromisoformat(transaction.date),
                                  transaction_value=transaction.value,
                                  transaction_type=transaction.type,
                                  transaction_category=transaction.category,
                                  transaction_description=transaction.description)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_total_by_category(db: Session, user_id: int, category: str, type: str):
    total = (
        db.query(func.sum(Transaction.transaction_value))
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_category == category,
            Transaction.transaction_type == type
        )
        .scalar()
    )
    return total or 0

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()

def get_transaction_by_user(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()

# TODO: funções de listar transações mas com filtros aplicados

def update_transaction(db: Session, transaction_id: int, transaction_new_data: TransactionCreate):
    transaction = get_transaction_by_id(db, transaction_id)
    if transaction:
        transaction.transaction_date = dt.fromisoformat(transaction_new_data.date)
        transaction.transaction_value = transaction_new_data.value
        transaction.transaction_type = transaction_new_data.type   # <-- FALTAVA
        transaction.transaction_category = transaction_new_data.category
        transaction.transaction_description = transaction_new_data.description
        
        db.commit()
        db.refresh(transaction)
        return transaction

    return None

def delete_transaction(db: Session, transaction_id: int):   
    transaction = get_transaction_by_id(db, transaction_id)
    if (transaction):
        db.delete(transaction)
        db.commit()

    