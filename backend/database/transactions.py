from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime as dt, date
from database.models import Transaction
from database.schemas import TransactionCreate

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

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()

def get_transactions_by_user(db: Session, user_id: int, transaction_type: str | None = None, transaction_category: str | None = None, start_date: date | None = None, end_date: date | None = None):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if (transaction_type):
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    if (transaction_category):
        query = query.filter(Transaction.transaction_category == transaction_category)
    
    if (start_date):
        query = query.filter(Transaction.transaction_date >= start_date)
    
    if (end_date):
        query = query.filter(Transaction.transaction_date <= end_date)
    
    return query.all()

def get_transaction_agregate(db: Session, user_id: int, transaction_type: str, start_date: date | None = None, end_date: date | None = None):
    transaction_agregate = db.query(Transaction.transaction_category, func.sum(Transaction.transaction_value))\
        .filter(Transaction.user_id == user_id)
    
    if (start_date):
        transaction_agregate = transaction_agregate.filter(Transaction.transaction_date >= start_date)
    
    if (end_date):
        transaction_agregate = transaction_agregate.filter(Transaction.transaction_date <= end_date)

    transaction_agregate = transaction_agregate.filter(Transaction.transaction_type == transaction_type)\
        .group_by(Transaction.transaction_category)\
        .all()
    
    if (transaction_agregate):
        return dict(transaction_agregate)
    else:
        return {}

def get_transaction_sum(db: Session, user_id: int, start_date: date | None = None, end_date: date | None = None):
    transactions_sum = db.query(Transaction.transaction_type, func.sum(Transaction.transaction_value))\
        .filter(Transaction.user_id == user_id)

    if (start_date):
        transactions_sum = transactions_sum.filter(Transaction.transaction_date >= start_date)
    
    if (end_date):
        transactions_sum = transactions_sum.filter(Transaction.transaction_date <= end_date)
        
    transactions_sum = transactions_sum.group_by(Transaction.transaction_type).all()    
    
    if (transactions_sum):
        transactions_sum = dict(transactions_sum)
        if ("Receita" not in transactions_sum):
            transactions_sum["Receita"] = 0
        if ("Despesa" not in transactions_sum):
            transactions_sum["Despesa"] = 0
        return transactions_sum
    else:
        return {"Receita": 0, "Despesa": 0}

def get_transactiom_sum_by_category(db: Session, user_id: int, start_date: date | None = None, end_date: date | None = None):
    transactions_sum = db.query(Transaction.transaction_type, Transaction.transaction_category, func.sum(Transaction.transaction_value))\
        .filter(Transaction.user_id == user_id)

    if (start_date):
        transactions_sum = transactions_sum.filter(Transaction.transaction_date >= start_date)
    
    if (end_date):
        transactions_sum = transactions_sum.filter(Transaction.transaction_date <= end_date)
        
    transactions_sum = transactions_sum.group_by(Transaction.transaction_type, Transaction.transaction_category).all()
    
    if (transactions_sum):
        return transactions_sum
    else:
        return []

def update_transaction(db: Session, transaction_id: int, transaction_new_data: TransactionCreate):
    transaction = get_transaction_by_id(db, transaction_id)
    if (transaction):
        transaction.transaction_date = dt.fromisoformat(transaction_new_data.date)
        transaction.transaction_value = transaction_new_data.value
        transaction.transaction_category = transaction_new_data.category
        transaction.transaction_description = transaction_new_data.description
        db.commit()
        db.refresh(transaction)

def delete_transaction(db: Session, transaction_id: int):   
    transaction = get_transaction_by_id(db, transaction_id)
    if (transaction):
        db.delete(transaction)
        db.commit()