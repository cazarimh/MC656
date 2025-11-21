from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database import transactions as crud_transactions
from database import users as crud_user
from database.schemas import TransactionCreate
from dto.transactions_dto import (
    TransactionRegisterResponse,
    TransactionsListResponse,
)
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
    transaction_model = crud_transactions.create_transaction_db(
        db, user.user_id, transaction_data
    )

    # Converte para o DTO de resposta
    return TransactionMapper.to_response(transaction_model)


def get_transactions_by_user(
    user_id: int, db: Session
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
    transactions_list = adapter.get_transactions(user_id)

    # Converte para a lista de DTOs de resposta
    return TransactionMapper.to_list_response(transactions_list)


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
    transaction = crud_transactions.get_transaction_by_id(db, transaction_id)
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
    crud_transactions.update_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_new_data=transaction_data
    )

    # Busca o objeto atualizado no banco para retornar
    updated_transaction_model = crud_transactions.get_transaction_by_id(
        db, transaction_id
    )

    # Converte para DTO e retorna
    return TransactionMapper.to_response(updated_transaction_model)


# --- FUNÇÃO 4: DELETE (Excluir) ---
def delete_specific_transaction(user_id: int, transaction_id: int, db: Session):
    # Usa a helper
    _get_transaction_and_verify_user(db, user_id, transaction_id)

    # Chama a função de delete do banco
    crud_transactions.delete_transaction(db, transaction_id)

    # Retorna uma mensagem de sucesso
    return {"detail": "Transaction successfully deleted"}
