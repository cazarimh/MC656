from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from .database.config import get_db
from .database.schemas import UserCreate, User, TransactionCreate, Transaction
from .database.users import create_user_db, get_user_by_email
from .utils.password_hash import get_password_hash
from .utils.validators import (
    validate_date_ISO_format,
    validate_email_format,
    validate_password_strength
)

app = FastAPI()


@app.post("/create-user", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Criação de um novo usuário no sistema

    Parâmetros:
    user_data (UserCreate): objeto contendo os dados do usuário, incluindo email e senha

    Retorna:
    User: objeto contendo o ID, nome, email e senha encriptada do usuário cadastrado

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


@app.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(user: User, expense: ExpenseCreate):
    """
    Criação de um novo gasto no sistema

    Parâmetros:
    user (User): objeto contendo o ID e o email do usuário cadastrado
    expense (ExpenseCreate): objeto contendo os dados para criação para os gastos
        - category: string contendo a categoria do gasto a ser cadastrado [Alimentação; Lazer; Contas]
        - date: string contendo a data do gasto. Deve estar em ISO String
        - value: float contendo o valor do gasto. Deve ser maior que zero

    Retorna:
    Expense: objeto contendo o ID, categoria, data e valor do gasto cadastrado, bem como o ID do usuário atrelado a ele

    Levanta:
    HTTPException:
        - 400 BAD REQUEST se a categoria informada não estiver entre [Alimentação; Lazer; Contas]
        - 400 BAD REQUEST se o valor informado for menor ou igual a zero
        - 400 BAD REQUEST se o formato da data informada não estiver em ISO String
        - 403 FORBIDDEN se o usuário não estiver cadastrado
    """
    global expenses_id

    if user.id in users_db:
        stored_user = users_db[user.id]

        if stored_user["email"] != user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="As credenciais do usuário (ID e Email) não correspondem.",
            )

        valid_categories = ["Alimentação", "Lazer", "Contas"]
        if expense.category not in valid_categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas].",
            )

        if expense.value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor informado é inválido. Informe um valor maior ou igual a zero.",
            )

        # Valida se a data está em formato ISO String
        validate_date_ISO_format(expense.date)

        new_expense = {
            "id": expenses_id,
            "user_id": user.id,
            "category": expense.category,
            "date": expense.date,
            "value": expense.value,
        }
        expenses_id += 1

        expenses_db[new_expense["id"]] = new_expense

        return new_expense
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado. Cadastre-se antes de registrar um gasto.",
        )


@app.get("/users/{user_id}/expenses", response_model=list[Expense])
def get_expenses_by_user(user_id: int):
    """
    Lista todos os gastos de um usuário específico

    Parâmetros:
    user_id (int): inteiro representando o id do usuário que queremos consultar os gastos

    Retorna:
    list[Expense]: uma list contendo todos os gatos do usuário
    Obs: retorna uma lista vazia caso o usuário não tenha nenhum gasto registrado

    Levanta:
    HTTPException:
        - 404 NOT FOUND se o usuário com o ID fornecido não foe encontrado
    """

    # Verifica se o usuário existe
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado.",
        )

    user_expenses = []
    for expense in (
        expenses_db.values()
    ):  # Para cada gasto cadastrado adiciona apenas do usuário desejado
        if expense["user_id"] == user_id:
            user_expenses.append(expense)

    return user_expenses
