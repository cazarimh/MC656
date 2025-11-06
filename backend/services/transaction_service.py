from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from backend.database import transactions as crud_transactions
from backend.database import users as crud_user
from backend.database.schemas import TransactionCreate

from backend.dto.transactions_dto import TransactionRegisterResponse, TransactionsListResponse
from backend.adapter.transactions_adapter import TransactionAdapter

from backend.utils.validators import validate_date_ISO_format

def create_new_transaction(
    user_id: int, 
    transaction_data: TransactionCreate, 
    db: Session
) -> TransactionRegisterResponse:
    
    # Valida o usuário
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado.",
        )

    # Validar o valor
    if transaction_data.value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valor informado é inválido. Informe um valor maior ou igual a zero.",
        )

    # Validar a data
    validate_date_ISO_format(transaction_data.date)

    # Chama o crud de transação
    transaction_model = crud_transactions.create_transaction_db(
        db, user.user_id, transaction_data
    )
    
    # Converte para o DTO de resposta
    return TransactionAdapter.to_response(transaction_model)

def get_transactions_by_user(
    user_id: int, 
    db: Session
) -> list[TransactionsListResponse]:
    
    # Valida o usuário
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )

    # Busca as transações
    transactions_list = crud_transactions.get_transaction_by_user(db, user.user_id)
    
    # Converte para a lista de DTOs de resposta
    return TransactionAdapter.to_list_response(transactions_list)

def _get_transaction_and_verify_user(
    db: Session, user_id: int, transaction_id: int
):
    """
    Busca o usuário, busca a transação,
    e verifica se a transação pertence ao usuário.
    Retorna o modelo da transação se tudo estiver OK.
    """
    # 1. Verifica se o usuário existe
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    # 2. Busca a transação
    transaction = crud_transactions.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Transaction not found"
        )
        
    # 3. VERIFICAÇÃO DE SEGURANÇA CRUCIAL
    if transaction.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this transaction"
        )
        
    return transaction

# --- FUNÇÃO 2: GET (Específico) ---
def get_specific_transaction(
    user_id: int, transaction_id: int, db: Session
) -> TransactionRegisterResponse:
    
    # Usa a função helper para buscar e verificar a transação
    transaction_model = _get_transaction_and_verify_user(
        db, user_id, transaction_id
    )
    
    # Converte para DTO e retorna
    return TransactionAdapter.to_response(transaction_model)

# --- FUNÇÃO 3: PUT (Editar) ---
def update_specific_transaction(
    user_id: int, 
    transaction_id: int, 
    transaction_data: TransactionCreate, 
    db: Session
) -> TransactionRegisterResponse:
    
    # Usa a helper para garantir que temos permissão
    _get_transaction_and_verify_user(db, user_id, transaction_id)
    
    # Valida os novos dados        
    if transaction_data.value <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido.")
        
    validate_date_ISO_format(transaction_data.date)

    # Chama a função de update do banco
    crud_transactions.update_transaction(
        db=db,
        transaction_id=transaction_id,
        new_date=transaction_data.date,
        new_value=transaction_data.value,
        new_category=transaction_data.category,
        new_description=transaction_data.description
    )
    
    # Busca o objeto atualizado no banco para retornar
    updated_transaction_model = crud_transactions.get_transaction_by_id(
        db, transaction_id
    )
    
    # Converte para DTO e retorna
    return TransactionAdapter.to_response(updated_transaction_model)

# --- FUNÇÃO 4: DELETE (Excluir) ---
def delete_specific_transaction(
    user_id: int, transaction_id: int, db: Session
):
    
    # Usa a helper
    _get_transaction_and_verify_user(db, user_id, transaction_id)
    
    # Chama a função de delete do banco
    crud_transactions.delete_transaction(db, transaction_id)
    
    # Retorna uma mensagem de sucesso
    return {"detail": "Transaction successfully deleted"}