from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.database import users as crud_user
from backend.database.schemas import UserCreate
from backend.dto.user_dto import UserLogin, UserRegisterResponse, UserResponse
from ..mapper.user_mapper import UserMapper
from backend.utils.password_hash import get_password_hash, verify_password

def create_new_user(user_data: UserCreate, db: Session) -> UserRegisterResponse:
    # Verificar se o email já existe
    db_user = crud_user.get_user_by_email(db, user_email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
        
    # Hashear a senha ANTES de salvar
    hashed_password = get_password_hash(user_data.password)
    
    # Cópia dos dados para não alterar o original
    user_data_to_db = user_data.model_copy()
    
    # Substituímos a senha pura pelo hash
    user_data_to_db.password = hashed_password
    
    # Chamamos o adapter para criar no banco
    new_user = crud_user.create_user_db(db, user=user_data_to_db)
    
    return UserMapper.to_register_response(new_user, "Success")

def authenticate_user(user_data: UserLogin, db: Session):
    # Busca o usuário pelo email
    db_user = crud_user.get_user_by_email(db, user_email=user_data.email)
    
    # Verifica se o usuário existe
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    # Verifica se a senha está correta
    if not verify_password(user_data.password, db_user.user_hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
        
    # Retorna o objeto do usuário se tudo estiver OK
    return db_user

# --- FUNÇÃO PARA OBTER DADOS DO USUÁRIO ---
def get_user_info(user_id: int, db: Session) -> UserResponse:
    # Busca usuário pelo ID
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    
    # Verifica se existe
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    # Retorna o usuário
    return UserMapper.to_response(db_user)