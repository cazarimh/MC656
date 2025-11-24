from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime as dt

from typing import Dict

from datetime import date

from services import transaction_service
from database.config import get_db

from database.schemas import TransactionCreate
from dto.transactions_dto import (
    TransactionRegisterResponse, 
    TransactionsListResponse
)
from dto.info_dto import TransactionInfoResponse

router = APIRouter(
    prefix="/{user_id}/transactions",
    tags=["2. Transações (Receitas e Despesas)"] 
)

@router.post(
    "/", # Rota: POST /{user_id}/transactions/
    response_model=TransactionRegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def create_transaction(
    user_id: int, 
    transaction_data: TransactionCreate, 
    db: Session = Depends(get_db)
):
    try:
        return transaction_service.create_new_transaction(
            user_id=user_id, transaction_data=transaction_data, db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/", # Rota: GET /{user_id}/transactions/?transaction_type=..&end_date=
    response_model=list[TransactionsListResponse]
)
def get_transactions(
    user_id: int,
    transaction_type: str | None = None,
    transaction_category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    try:

        return transaction_service.get_transactions_by_user(user_id=user_id,
                                                         db=db,
                                                         transaction_type=transaction_type,
                                                         transaction_category=transaction_category,
                                                         start_date=start_date,
                                                         end_date=end_date)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/info", # Rota: GET /{user_id}/transactions/?transaction_type=..&end_date=
    response_model=TransactionInfoResponse
)
def get_transactions_info(
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    try:
        return transaction_service.get_transactions_info(user_id=user_id,
                                                         db=db,
                                                         start_date=start_date,
                                                         end_date=end_date)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/{transaction_id}", # Rota: GET /{id}/transactions/{id}
    response_model=TransactionRegisterResponse
)
def get_transaction(
    user_id: int, 
    transaction_id: int, 
    db: Session = Depends(get_db)
):
    try:
        return transaction_service.get_specific_transaction(
            user_id=user_id, transaction_id=transaction_id, db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA 4: PUT (Editar) ---
@router.put(
    "/{transaction_id}", # Rota: PUT /{id}/transactions/{id}
    response_model=TransactionRegisterResponse
)
def update_transaction(
    user_id: int, 
    transaction_id: int, 
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):
    try:
        return transaction_service.update_specific_transaction(
            user_id=user_id, 
            transaction_id=transaction_id, 
            transaction_data=transaction_data, 
            db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA 5: DELETE (Excluir) ---
@router.delete(
    "/{transaction_id}", # Rota: DELETE /{id}/transactions/{id}
    response_model=Dict[str, str]
)
def delete_transaction(
    user_id: int, 
    transaction_id: int, 
    db: Session = Depends(get_db)
):
    try:
        return transaction_service.delete_specific_transaction(
            user_id=user_id, transaction_id=transaction_id, db=db
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
