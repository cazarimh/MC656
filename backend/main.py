from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .controller import user_controller
from .controller import transaction_controller
from .adapter.transactions_adapter import TransactionAdapter
from .adapter.user_adapter import UserAdapter
from .database import models
from .database.config import engine, get_db
from .database.schemas import (
    TransactionCreate,
    UserCreate,
)
from .database.users import create_user_db, get_user_by_id
from .database.transactions import create_transaction_db, get_transaction_by_user
from .dto.transactions_dto import TransactionRegisterResponse, TransactionsListResponse
from .dto.user_dto import UserRegisterResponse
from .utils.password_hash import get_password_hash
from .utils.validators import TransactionValidator as tv
from .utils.validators import PasswordValidator as pv
from .utils.validators import (
    validate_date_ISO_format,
    validate_email_format,
    validate_unique_email,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(
    "/users", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Criação de um novo usuário no sistema

    Parâmetros:
    user_data (UserCreate): objeto contendo os dados do usuário, incluindo email e senha

    Retorna:
    UserResponse: objeto contendo o ID, nome, email e senha encriptada do usuário cadastrado

    Levanta:
    HTTPException:
        - 400 BAD REQUEST se o campo nome estiver vazio
        - 400 BAD REQUEST se o email já estiver cadastrado
        - 400 BAD REQUEST se o formato do email não for válido ou a senha não atender os critérios de segurança
    """

    if not user_data.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insira um nome.",
        )

    validate_email_format(user_data.email)

    validate_unique_email(db, user_data.email)

    pv.validate_password_strength(user_data.password)

    user_data.password = get_password_hash(user_data.password)

    user = create_user_db(db, user_data)
    return UserAdapter.to_register_response(user, "Success")


@app.post(
    "/{user_id}/transactions",
    response_model=TransactionRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    user_id: int, transaction_create: TransactionCreate, db: Session = Depends(get_db)
):
    """
    Criação de uma nova transação no sistema

    Parâmetros:
    user_id (int): ID do usuário logado
    transaction (TransactionCreate): objeto contendo os dados para criação das transações
        - date: string contendo a data da transação. Deve estar em ISO String
        - value: float contendo o valor da transação. Deve ser maior que zero
        - type: string contendo o tipo da transação a ser cadastrada [Receita; Despesa]
        - category: string contendo a categoria da transação a ser cadastrado [Alimentação; Lazer; Contas]
        - description: string contendo uma breve descrição da transação a ser cadastrada

    Retorna:
    TransactionResponse: objeto contendo o ID, data, valor, tipo, categoria, e descrição da transação cadastrado, bem como o ID do usuário atrelado a ela

    Levanta:
    HTTPException:
        - 400 BAD REQUEST se o formato da data informada não estiver em ISO String
        - 400 BAD REQUEST se o valor informado for menor ou igual a zero
        - 400 BAD REQUEST se o tipo informado não estiver entre [Receita; Despesa]
        - 400 BAD REQUEST se a categoria informada não estiver entre [Alimentação; Lazer; Contas]
        - 403 FORBIDDEN se o usuário não estiver cadastrado
    """

    user = get_user_by_id(db, user_id)
    if user:

        tv.validate_transaction_type(transaction_create)

        tv.validate_transaction_category(transaction_create)
        
        tv.validate_transaction_value(transaction_create)

        validate_date_ISO_format(transaction_create.date)

        new_transaction = create_transaction_db(db, user.user_id, transaction_create)
        return TransactionAdapter.to_response(new_transaction)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado. Cadastre-se antes de registrar um gasto.",
        )


@app.get("/{user_id}/transactions", response_model=list[TransactionsListResponse])
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    """
    Lista todos os gastos de um usuário específico

    Parâmetros:
    user_id (int): inteiro representando o id do usuário que queremos consultar os gastos

    Retorna:
    list[TransactionResponse]: uma list contendo todos os gatos do usuário
    Obs: retorna uma lista vazia caso o usuário não tenha nenhum gasto registrado

    Levanta:
    HTTPException:
        - 404 NOT FOUND se o usuário com o ID fornecido não for encontrado
    """

    user = get_user_by_id(db, user_id)
    if user:
        transactions = get_transaction_by_user(db, user.user_id)
        return TransactionAdapter.to_list_response(transactions)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )


app.include_router(user_controller.router)
app.include_router(transaction_controller.router)