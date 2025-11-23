from sqlalchemy.orm import Session
from database.models import Transaction
import calendar
from collections import defaultdict

# ==============
# MENSAL
# ==============
def get_monthly_summary(db: Session, user_id: int):
    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .all()

    monthly = defaultdict(lambda: {"receita": 0, "despesa": 0})

    for t in transactions:
        mes_num = int(t.transaction_date.month)
        mes_nome = calendar.month_abbr[mes_num].capitalize()

        if t.transaction_type == "Receita":
            monthly[mes_nome]["receita"] += t.transaction_value
        else:
            monthly[mes_nome]["despesa"] += t.transaction_value

    # ordenar por mês
    ordered = []
    for i in range(1, 13):
        mes_nome = calendar.month_abbr[i].capitalize()
        ordered.append({
            "mes": mes_nome,
            "receita": monthly[mes_nome]["receita"],
            "despesa": monthly[mes_nome]["despesa"],
        })

    return ordered


# ==============
# DESPESAS POR CATEGORIA
# ==============
def get_expenses_by_category(db: Session, user_id: int):
    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == user_id,
                Transaction.transaction_type == "Despesa")\
        .all()

    categorias = defaultdict(float)

    for t in transactions:
        categorias[t.transaction_category] += t.transaction_value

    return [
        {"name": cat, "value": total}
        for cat, total in categorias.items()
    ]

# ==============
# RECEITAS POR CATEGORIA
# ==============
def get_income_by_category(db: Session, user_id: int):
    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == user_id,
                Transaction.transaction_type == "Receita")\
        .all()

    categorias = defaultdict(float)

    for t in transactions:
        categorias[t.transaction_category] += t.transaction_value

    return [
        {"name": cat, "value": total}
        for cat, total in categorias.items()
    ]
