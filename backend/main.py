from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from .database import models
from .database.config import engine, get_db
from .database.schemas import UserCreate, UserResponse, TransactionCreate, TransactionResponse
from .database.users import create_user_db, get_user_by_email, get_user_by_id
from .database.transactions import create_transaction_db, get_transaction_by_user
from .utils.password_hash import get_password_hash
from .utils.validators import (
    validate_date_ISO_format,
    validate_email_format,
    validate_password_strength
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Criação de um novo usuário no sistema

    Parâmetros:
    user_data (UserCreate): objeto contendo os dados do usuário, incluindo email e senha

    Retorna:
    UserResponse: objeto contendo o ID, nome, email e senha encriptada do usuário cadastrado

    Levanta:
    HTTPException:
        - 400 BAD REQUEST se o email já estiver cadastrado
        - 400 BAD REQUEST se o formato do email não for válido ou a senha não atender os critérios de segurança
    """

    # Valida o formato do email
    validate_email_format(user_data.email)

    # Verifica se o email já existe no banco
    if (get_user_by_email(db, user_data.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está cadastrado.",
        )

    # Valida se a senha preenche os critérios
    validate_password_strength(user_data.password)

    # Gera o hash da senha para não armazenar a senha original
    user_data.password = get_password_hash(user_data.password)

    return create_user_db(db, user_data)


@app.post("/{user_id}/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(user_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
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
    if (user):

        valid_types = ["Receita", "Despesa"]
        if transaction.type not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo informado é inválido. Informe um entre [Receita; Despesa].",
            )
        
        valid_categories = ["Alimentação", "Lazer", "Contas"]
        if transaction.category not in valid_categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas].",
            )

        if transaction.value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor informado é inválido. Informe um valor maior ou igual a zero.",
            )

        # Valida se a data está em formato ISO String
        validate_date_ISO_format(transaction.date)

        return create_transaction_db(db, user.user_id, transaction)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado. Cadastre-se antes de registrar um gasto.",
        )


@app.get("/{user_id}/transactions", response_model=list[TransactionResponse])
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
    if (user):
        return get_transaction_by_user(db, user.user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )
