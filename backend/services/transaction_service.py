from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from dateutil.relativedelta import relativedelta

from database import transactions as crud_transaction
from database import users as crud_user
from database.schemas import TransactionCreate
from dto.transactions_dto import (
    TransactionRegisterResponse,
    TransactionsListResponse,
)
from dto.info_dto import TransactionInfoResponse
from utils.validators import validate_date_ISO_format

from adapter.transactions_adapter import TransactionAdapter
from mapper.transactions_mapper import TransactionMapper

from utils.validators import (
    FieldValidator as val,
    validate_date_ISO_format
)

def create_new_transaction(
    user_id: int, transaction_data: TransactionCreate, db: Session
) -> TransactionRegisterResponse:
    # Valida o usuário
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado.",
        )

    # Validações
    val.validate_type(transaction_data.type)

    val.validate_category(transaction_data.category, transaction_data.type)
    
    val.validate_value(transaction_data.value)

    validate_date_ISO_format(transaction_data.date)

    # Chama o crud de transação
    transaction_model = crud_transaction.create_transaction_db(
        db, user.user_id, transaction_data
    )

    # Converte para o DTO de resposta
    return TransactionMapper.to_response(transaction_model)


def get_transactions_by_user(
    user_id: int,
    db: Session,
    transaction_type: str | None = None,
    transaction_category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
) -> list[TransactionsListResponse]:
    # Valida o usuário
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )

    # Busca as transações
    adapter = TransactionAdapter(db)
    transactions_list = adapter.get_transactions(user_id=user_id,
                                                 transaction_type=transaction_type,
                                                 transaction_category=transaction_category,
                                                 start_date=start_date,
                                                 end_date=end_date)

    # Converte para a lista de DTOs de resposta
    return TransactionMapper.to_list_response(transactions_list)


def get_transactions_info(
    user_id: int,
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None
) -> TransactionInfoResponse:

    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )
    
    incomeDict = crud_transaction.get_transaction_agregate(db, user_id, "Receita", start_date, end_date)
    incomeList = [
        { "transaction_category": transaction_category, "transaction_value": transaction_value} for transaction_category, transaction_value in incomeDict.items()
    ]

    expenseDict = crud_transaction.get_transaction_agregate(db, user_id, "Despesa", start_date, end_date)
    expenseList = [
        { "transaction_category": transaction_category, "transaction_value": transaction_value} for transaction_category, transaction_value in expenseDict.items()
    ]
    
    start_date = end_date - relativedelta(months=11)
    start_date = start_date.replace(day=1)

    transactions_list = []
    for i in range(12):
        lower = start_date + relativedelta(months=i)
        upper = (start_date + relativedelta(months=i+1)) - relativedelta(days=1)

        month_transactions = crud_transaction.get_transaction_sum(db=db,
                                                                   user_id=user.user_id,
                                                                   start_date=lower,
                                                                   end_date=upper)
        
        transactions_list.append({ "transaction_month": months[lower.month-1],
                                  "month_income": month_transactions["Receita"],
                                  "month_expense": month_transactions["Despesa"]})

    return TransactionInfoResponse(lastYearTransactions=transactions_list,
                                   incomeList=incomeList,
                                   expenseList=expenseList)

def _get_transaction_and_verify_user(db: Session, user_id: int, transaction_id: int):
    """
    Busca o usuário, busca a transação,
    e verifica se a transação pertence ao usuário.
    Retorna o modelo da transação se tudo estiver OK.
    """
    # 1. Verifica se o usuário existe
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # 2. Busca a transação
    transaction = crud_transaction.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    # 3. VERIFICAÇÃO DE SEGURANÇA CRUCIAL
    if transaction.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this transaction",
        )

    return transaction


# --- FUNÇÃO 2: GET (Específico) ---
def get_specific_transaction(
    user_id: int, transaction_id: int, db: Session
) -> TransactionRegisterResponse:
    # Usa a função helper para buscar e verificar a transação
    # 1. Verifica se o usuário existe
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Busca as transações
    adapter = TransactionAdapter(db)
    transactions_list = adapter.get_transactions(user_id)

    transactions = TransactionMapper.to_list_response(transactions_list)
    for t in transactions:
        if t.transaction_id == transaction_id:
            return t
    
    raise HTTPException(status_code=404, detail="Transação Não Encontrada.")


# --- FUNÇÃO 3: PUT (Editar) ---
def update_specific_transaction(
    user_id: int, transaction_id: int, transaction_data: TransactionCreate, db: Session
) -> TransactionRegisterResponse:
    # Usa a helper para garantir que temos permissão
    _get_transaction_and_verify_user(db, user_id, transaction_id)
    
    val.validate_type(transaction_data.type)

    val.validate_category(transaction_data.category, transaction_data.type)
    
    val.validate_value(transaction_data.value)
        
    validate_date_ISO_format(transaction_data.date)

    # Chama a função de update do banco
    crud_transaction.update_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_new_data=transaction_data
    )

    # Busca o objeto atualizado no banco para retornar
    updated_transaction_model = crud_transaction.get_transaction_by_id(
        db, transaction_id
    )

    # Converte para DTO e retorna
    return TransactionMapper.to_response(updated_transaction_model)


# --- FUNÇÃO 4: DELETE (Excluir) ---
def delete_specific_transaction(user_id: int, transaction_id: int, db: Session):
    # Usa a helper
    _get_transaction_and_verify_user(db, user_id, transaction_id)

    # Chama a função de delete do banco
    crud_transaction.delete_transaction(db, transaction_id)

    # Retorna uma mensagem de sucesso
    return {"detail": "Transaction successfully deleted"}
