from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.config import get_db
from backend.database.schemas import UserCreate, UserResponse
from backend.services import user_service
from backend.adapter.user_adapter import  UserLogin, UserLoginResponse 

router = APIRouter(
    prefix="/users",
    tags=["1. Autenticação e Usuários"]
)

@router.post(
    "/", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    
    # Controller recebe a requisição HTTP (user_data)
    try:
        new_user = user_service.create_new_user(user_data=user_data, db=db)
        return new_user
    
    # Se o serviço levantar uma exceção (como email duplicado),
    # o controller a captura e a retorna como um erro HTTP.
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
        user = user_service.get_user_info(user_id=user_id, db=db)
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