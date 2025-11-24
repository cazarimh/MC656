from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from database.config import get_db
from database.schemas import UserCreate
from services import user_service
from dto.user_dto import  UserLogin, UserLoginResponse , UserResponse, UserRegisterResponse
from dto.info_dto import UserInfoResponse

from database.goals import get_general_goals

router = APIRouter(
    prefix="/users",
    tags=["1. Autenticação e Usuários"]
)

@router.post(
    "/", 
    response_model=UserRegisterResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    
    # Controller recebe a requisição HTTP (user_data)
    try:
        # O serviço agora já retorna o DTO pronto
        return user_service.create_new_user(user_data=user_data, db=db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
@router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK
)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    
    # Recebe email/senha
    try:
        authenticated_user = user_service.authenticate_user(
            user_data=user_data, 
            db=db
        )
        
        # Retorna o ID do usuário, como você pediu
        return UserLoginResponse(user_id=authenticated_user.user_id)
    
    except HTTPException as e:
        # Captura os erros (404, 401) do serviço
        raise e
    except Exception as e:
        # Captura de erro genérico
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# --- ROTA PARA OBTER DADOS DO USUÁRIO ---
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    
    # Recebe user_id da URL
    # Passa para o Service
    try:
        user = user_service.get_user(user_id=user_id, db=db)
        return user
    
    except HTTPException as e:
        # Captura o erro 404 do serviço
        raise e
    except Exception as e:
        # Captura de erro genérico
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/{user_id}/info",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK
)
def get_user_info(
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    try:
        user_info = user_service.get_user_info(user_id=user_id, db=db, start_date=start_date, end_date=end_date)
        return user_info
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )