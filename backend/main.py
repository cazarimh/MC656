from fastapi import FastAPI, HTTPException, status
from .models.userCreate import UserCreate
from .models.user import User
from .models.expenseCreate import ExpenseCreate
from .models.expense import Expense
from .utils.password_hash import get_password_hash
from .utils.validators import validate_email_format, validate_password_strength, validate_date_ISO_format

app = FastAPI()

# "Banco de Dados" em memória (apenas para testes)
dict_db = {}
user_id = 0

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    '''
    Criação de um novo usuário no sistema

    Parâmetros:
    user_data (UserCreate): objeto contendo os dados do usuário, incluindo email e senha

    Retorna:
    User: objeto contendo o ID e o email do usuário cadastrado

    Levanta:
    HTTPException:
        - 400 BAD REQUEST se o email já estiver cadastrado
        - 400 BAD REQUEST se o formato do email não for válido ou a senha não atender os critérios de segurança
    '''
    global user_id

    # Valida o formato do email
    validate_email_format(user_data.email)

    # Valida se a senha preenche os critérios
    validate_password_strength(user_data.password)

    # Verifica se o email já existe no "banco"
    for user in dict_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email já está cadastrado."
            )
    
    # Gera o hash da senha para não armazenar a senha original
    hashed_password = get_password_hash(user_data.password)
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password 
    }
    user_id += 1

    # Armazena o novo usuário no dicionário
    dict_db[new_user["id"]] = new_user

    # Retorna os dados do usuário, seguindo o modelo User definido em models
    return new_user

# "Banco de Dados" de um usuário X em memória (apenas para testes)
expenses_db = {}
expenses_id = 0

@app.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(user: User, expense: ExpenseCreate):
    '''
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
    '''
    global expenses_id

    if (user.id in dict_db):

        stored_user = dict_db[user.id]

        if stored_user["email"] != user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="As credenciais do usuário (ID e Email) não correspondem."
            )
 
        valid_categories = ["Alimentação", "Lazer", "Contas"]
        if (expense.category not in valid_categories):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas]."
            )

        if (expense.value <= 0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor informado é inválido. Informe um valor maior ou igual a zero."
            )

        # Valida se a data está em formato ISO String
        validate_date_ISO_format(expense.date)
        
        new_expense = {
            "id": expenses_id,
            "user_id": user.id,
            "category": expense.category,
            "date": expense.date,
            "value": expense.value
        }
        expenses_id += 1

        expenses_db[new_expense["id"]] = new_expense

        return new_expense
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado. Cadastre-se antes de registrar um gasto."
        )