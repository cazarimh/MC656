from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session

from controller import goal_controller
from controller import transaction_controller
from controller import user_controller

# from adapter.transactions_adapter import TransactionAdapter

# from mapper.goals_mapper import GoalMapper
# from mapper.user_mapper import UserMapper
# from mapper.transactions_mapper import TransactionMapper

from database import models
from database.config import engine, get_db
# from database.schemas import (
#     GoalCreate,
#     TransactionCreate,
#     UserCreate,
# )
# from database.goals import create_goal_db, get_goal_by_user
# from database.transactions import create_transaction_db, get_transaction_by_user
# from database.users import create_user_db, get_user_by_id

# from dto.goals_dto import GoalRegisterResponse, GoalsListResponse
# from dto.transactions_dto import TransactionRegisterResponse, TransactionsListResponse
# from dto.user_dto import UserRegisterResponse

# from utils.password_hash import get_password_hash
# from utils.validators import FieldValidator as val
# from utils.validators import PasswordValidator as pv
# from utils.validators import (
#     validate_date_ISO_format,
#     validate_email_format,
#     validate_unique_email,
# )

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_controller.router)
app.include_router(transaction_controller.router)
app.include_router(goal_controller.router)


# """
# Criação de um novo usuário no sistema

# Parâmetros:
# user_data (UserCreate): objeto contendo os dados do usuário, incluindo email e senha

# Retorna:
# UserResponse: objeto contendo o ID, nome, email e senha encriptada do usuário cadastrado

# Levanta:
# HTTPException:
#     - 400 BAD REQUEST se o campo nome estiver vazio
#     - 400 BAD REQUEST se o email já estiver cadastrado
#     - 400 BAD REQUEST se o formato do email não for válido ou a senha não atender os critérios de segurança
# """

# @app.post("/{user_id}/transactions", response_model=TransactionRegisterResponse, status_code=status.HTTP_201_CREATED)
# def create_transaction(user_id: int, transaction_create: TransactionCreate, db: Session = Depends(get_db)):
#     """
#     Criação de uma nova transação no sistema

#     Parâmetros:
#     user_id (int): ID do usuário logado
#     transaction_create (TransactionCreate): objeto contendo os dados para criação das transações
#         - date: string contendo a data da transação. Deve estar em ISO String
#         - value: float contendo o valor da transação. Deve ser maior que zero
#         - type: string contendo o tipo da transação a ser cadastrada [Receita; Despesa]
#         - category: string contendo a categoria da transação a ser cadastrada
#         - description: string contendo uma breve descrição da transação a ser cadastrada

#     Retorna:
#     TransactionRegisterResponse: objeto contendo o ID, data, valor, tipo, categoria, e descrição da transação cadastrada, bem como o ID do usuário atrelado a ela

#     Levanta:
#     HTTPException:
#         - 400 BAD REQUEST se o formato da data informada não estiver em ISO String
#         - 400 BAD REQUEST se o valor informado for menor ou igual a zero
#         - 400 BAD REQUEST se o tipo informado não estiver entre [Receita; Despesa]
#         - 400 BAD REQUEST se a categoria informada não estiver dentre as válidas
#         - 403 FORBIDDEN se o usuário não estiver cadastrado
#     """

#     user = get_user_by_id(db, user_id)
#     if user:

#         val.validate_type(transaction_create.type)

#         val.validate_category(transaction_create.category, transaction_create.type)
        
#         val.validate_value(transaction_create.value)

#         validate_date_ISO_format(transaction_create.date)

#         new_transaction = create_transaction_db(db, user.user_id, transaction_create)
#         return TransactionAdapter.to_response(new_transaction)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Usuário não cadastrado. Cadastre-se antes de registrar um gasto.",
#         )


# @app.get("/{user_id}/transactions", response_model=list[TransactionsListResponse])
# def get_transactions(user_id: int, db: Session = Depends(get_db)):
#     """
#     Lista todas as transações de um usuário específico

#     Parâmetros:
#     user_id (int): inteiro representando o id do usuário que queremos consultar as transações

#     Retorna:
#     list[TransactionsListResponse]: uma list contendo todas as transações do usuário
#     Obs: retorna uma lista vazia caso o usuário não tenha nenhuma transação registrada

#     Levanta:
#     HTTPException:
#         - 404 NOT FOUND se o usuário com o ID fornecido não for encontrado
#     """

#     user = get_user_by_id(db, user_id)
#     if user:
#         transaction_adapter = TransactionAdapter(db)
#         transactions = transaction_adapter.get_transactions(user.user_id)
#         return TransactionMapper.to_list_response(transactions)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Usuário com ID {user_id} não encontrado.",
#         )


# @app.post("/{user_id}/goals", response_model=GoalRegisterResponse, status_code=status.HTTP_201_CREATED)
# def create_goal(user_id: int, goal_create: GoalCreate, db: Session = Depends(get_db)):
#     """
#     Criação de uma nova meta no sistema

#     Parâmetros:
#     user_id (int): ID do usuário logado
#     goal_create (GoalCreate): objeto contendo os dados para criação das metas
#         - value: float contendo o valor da meta. Deve ser maior que zero
#         - type: string contendo o tipo da meta a ser cadastrada [Receita; Despesa]
#         - category: string contendo a categoria da meta a ser cadastrada

#     Retorna:
#     GoalRegisterResponde: objeto contendo o ID, valor, tipo e categoria da meta cadastrada, bem como o ID do usuário atrelado a ela

#     Levanta:
#     HTTPException:
#         - 400 BAD REQUEST se o valor informado for menor ou igual a zero
#         - 400 BAD REQUEST se o tipo informado não estiver entre [Receita; Despesa]
#         - 400 BAD REQUEST se a categoria informada não estiver dentre as válidas
#         - 403 FORBIDDEN se o usuário não estiver cadastrado
#     """

#     user = get_user_by_id(db, user_id)
#     if user:

#         val.validate_type(goal_create.type)

#         val.validate_category(goal_create.category)
        
#         val.validate_value(goal_create.value)

#         new_goal = create_goal_db(db, user.user_id, goal_create)
#         return GoalAdapter.to_response(new_goal)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Usuário não cadastrado. Cadastre-se antes de registrar uma meta.",
#         )


# @app.get("/{user_id}/goals", response_model=list[GoalsListResponse])
# def get_goals(user_id: int, db: Session = Depends(get_db)):
#     """
#     Lista todas as metas de um usuário específico

#     Parâmetros:
#     user_id (int): inteiro representando o id do usuário que queremos consultar as metas

#     Retorna:
#     list[GoalsListResponse]: uma list contendo todas as metas do usuário
#     Obs: retorna uma lista vazia caso o usuário não tenha nenhuma meta registrada

#     Levanta:
#     HTTPException:
#         - 404 NOT FOUND se o usuário com o ID fornecido não for encontrado
#     """

#     user = get_user_by_id(db, user_id)
#     if user:
#         goals = get_goal_by_user(db, user.user_id)
#         return GoalAdapter.to_list_response(goals)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Usuário com ID {user_id} não encontrado.",
#         )
