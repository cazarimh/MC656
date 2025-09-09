import re
from datetime import datetime as dt
from fastapi import HTTPException, status

def validate_password_strength(password: str):
    '''
    Verifica a validade da senha baseada nos critérios abaixo:
    - Conter ao menos 8 caracteres
    - Conter ao menos uma letra maiúscula
    - Conter ao menos uma letra minúscula
    - Conter ao menos um caractere especial
    - Conter ao menos um dígito
    
    Parâmetros:
    password: (string): string da password cadastrada pelo usuário

    Retorna:
    None

    Levanta:
    HTTPException: se a senha não atender algum critério
    '''
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter ao menos 8 caracteres.",
        )
    
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter ao menos uma letra maiúscula.",
        )

    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter ao menos uma letra minúscula.",
        )
    
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter ao menos um dígito.",
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos um caractere especial.",
        )

    # Retorna nulo caso todas as verificações forem válidas
    return None

def validate_email_format(email: str):
    '''
    Verifica se o email cadastrado possui formato válido

    Parâmetros:
    email (string): string do email cadastrado pelo usuário

    Retorna:
    None

    Levanta:
    HTTPException: se o formato do email for inválido
    '''
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O formato do email é inválido.",
        )

    # Retorna nulo caso o email seja válido
    return None

def validate_date_ISO_format(date: str):
    '''
    Verifica se a data cadastrada segue o formato válido (ISO String)

    Parâmetros:
    date (string): string da data informada pelo usuário

    Retorna:
    None

    Levanta:
    HTTPException: se o formato da data for inválido ou se a data informada for no futuro
    '''
    try:
        validation_date = dt.fromisoformat(date)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O formato da data informada é inválido. O formato esperado é YYYY-MM-DD (ou outro no formato ISO)",
        )
    
    if (validation_date.tzinfo == None):
        today = dt.now()
    else:
        today = dt.now(tz=validation_date.tzinfo)
    
    if (validation_date > today):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data informada é no futuro. Informe uma data até o dia atual.",
        )
    
    # Retorna nulo cado a data seja válida
    return None