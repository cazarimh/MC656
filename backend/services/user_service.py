from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from database import users as crud_user
from database import transactions as crud_transaction
from database import goals as crud_goal

from database.schemas import UserCreate
from dto.user_dto import UserLogin, UserRegisterResponse, UserResponse
from dto.info_dto import UserInfoResponse
from mapper.user_mapper import UserMapper
from utils.validators import (
    validate_email_format,
    validate_unique_email,
    PasswordValidator as pv
)
from utils.password_hash import get_password_hash, verify_password

def create_new_user(user_data: UserCreate, db: Session) -> UserRegisterResponse:
    if not user_data.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insira um nome.",
        )
    

    validate_email_format(user_data.email)

    validate_unique_email(db, user_data.email)

    pv.validate_password_strength(user_data.password)
        
    user_data_to_db = user_data.model_copy()
    
    user_data_to_db.password = get_password_hash(user_data.password)
    
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
def get_user(user_id: int, db: Session) -> UserResponse:
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

def get_user_info(user_id: int, db: Session, start_date: date | None = None, end_date: date | None = None) -> UserInfoResponse:
    db_user = crud_user.get_user_by_id(db, user_id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    userTransactions = crud_transaction.get_transaction_sum(db, user_id, start_date, end_date)
    financialData = {
        "totalIncome": userTransactions["Receita"],
        "totalExpense": userTransactions["Despesa"],
        "currentBalance": userTransactions["Receita"] - userTransactions["Despesa"],
    }

    userGoals = crud_goal.get_general_goals(db, user_id)
    generalGoals = [
        { "goal_type": goal_type, "goal_value": goal_value} for goal_type, goal_value in userGoals.items()
    ]

    incomeDict = crud_transaction.get_transaction_agregate(db, user_id, "Receita", start_date, end_date)
    incomeList = [
        { "transaction_category": transaction_category, "transaction_value": transaction_value} for transaction_category, transaction_value in incomeDict.items()
    ]

    expenseDict = crud_transaction.get_transaction_agregate(db, user_id, "Despesa", start_date, end_date)
    expenseList = [
        { "transaction_category": transaction_category, "transaction_value": transaction_value} for transaction_category, transaction_value in expenseDict.items()
    ]
    
    return UserInfoResponse(financialData=financialData,
                            generalGoals=generalGoals,
                            incomeList=incomeList,
                            expenseList=expenseList)