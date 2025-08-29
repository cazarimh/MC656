from fastapi import FastAPI, HTTPException, status
from .models import UserCreate, UserOut
from .password_hash import get_password_hash
from .validators import validate_email_format, validate_password_strength

app = FastAPI()

# "Banco de Dados" em memória (apenas para testes)
dict_db = {}
user_id = 0

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    '''
    Criação de um novo usuário no sistema

    Parâmetros:
    user_data (UserCreate): objeto contendo os dados do usuário, incluindo email e senha

    Retorna:
    UserOut: objeto contendo o ID e o email do usuário cadastrado

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
    user_id += 1
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password 
    }

    # Armazena o novo usuário no dicionário
    dict_db[new_user["id"]] = new_user

    # Retorna os dados do usuário, seguindo o modelo UserOut definido em models
    return new_user