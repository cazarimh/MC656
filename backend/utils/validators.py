import re
from datetime import datetime as dt
from fastapi import HTTPException, status

class TransactionValidator:
    from database.schemas import TransactionCreate

    @staticmethod
    def validate_transaction_type(transaction: TransactionCreate):
        '''
        Verifica se o tipo da transação é um entre [Receita, Despesa]
        
        Parâmetros:
        transaction (TransactionCreate): informações para criação da transação

        Retorna:
        None

        Levanta:
        HTTPException: se o tipo for inválido
        '''
        valid_types = ["Receita", "Despesa"]
        if transaction.type not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo informado é inválido. Informe um entre [Receita, Despesa].",
            )
        
        # Retorna nulo caso todas as verificações forem válidas
        return None

    @staticmethod
    def validate_transaction_category(transaction: TransactionCreate):
        '''
        Verifica se a categoria da transação é um entre
        - [Salário, Freelance, Investimentos, Outros] para Receita
        - [Moradia, Alimentação, Transporte, Entretenimento, Utilidades, Saúde, Educação, Outros] para Despesa
        
        Parâmetros:
        transaction (TransactionCreate): informações para criação da transação

        Retorna:
        None

        Levanta:
        HTTPException: se a categoria for inválida
        '''
        valid_categories = {"Receita": ["Salário", "Freelance", "Investimentos", "Outros"],
                            "Despesa":["Moradia", "Alimentação", "Transporte", "Entretenimento", "Utilidades", "Saúde", "Educação", "Outros"]}

        if transaction.category not in valid_categories[transaction.type]:
            if transaction.type == "Receita":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Categoria informada é inválida. Informe uma entre [Salário, Freelance, Investimentos, Outros].",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Categoria informada é inválida. Informe uma entre [Moradia, Alimentação, Transporte, Entretenimento, Utilidades, Saúde, Educação, Outros].",
                )
        
        # Retorna nulo caso todas as verificações forem válidas
        return None

    @staticmethod
    def validate_transaction_value(transaction: TransactionCreate):
        '''
        Verifica se o valor da transação é um número positivo
        
        Parâmetros:
        transaction (TransactionCreate): informações para criação da transação

        Retorna:
        None

        Levanta:
        HTTPException: se o valor for inválido
        '''
        if transaction.value <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Valor informado é inválido. Informe um valor maior ou igual a zero.",
                )
        
        # Retorna nulo caso todas as verificações forem válidas
        return None

class PasswordValidator:

    @staticmethod
    def __verify_length(password: str):
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter ao menos 8 caracteres.",
            )

        # Retorna nulo caso todas as verificações forem válidas
        return None
        
    @staticmethod
    def __verify_upper_case(password: str):
        if not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter ao menos uma letra maiúscula.",
            )

        # Retorna nulo caso todas as verificações forem válidas
        return None
    
    @staticmethod
    def __verify_lower_case(password: str):
        if not re.search(r"[a-z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter ao menos uma letra minúscula.",
            )

        # Retorna nulo caso todas as verificações forem válidas
        return None
    
    @staticmethod
    def __verify_number(password: str):
        if not re.search(r"\d", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter ao menos um dígito.",
            )

        # Retorna nulo caso todas as verificações forem válidas
        return None
    
    @staticmethod
    def __verify_special_char(password: str):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos um caractere especial.",
            )

        # Retorna nulo caso todas as verificações forem válidas
        return None
    
    @staticmethod
    def validate_password_strength(password: str):
        '''
        Verifica a validade da senha baseada nos critérios abaixo:
        - Conter ao menos 8 caracteres
        - Conter ao menos uma letra maiúscula
        - Conter ao menos uma letra minúscula
        - Conter ao menos um caractere especial
        - Conter ao menos um dígito
        
        Parâmetros:
        password (string): string da password cadastrada pelo usuário

        Retorna:
        None

        Levanta:
        HTTPException: se a senha não atender algum critério
        '''

        PasswordValidator.__verify_length(password)
        PasswordValidator.__verify_upper_case(password)
        PasswordValidator.__verify_lower_case(password)
        PasswordValidator.__verify_number(password)
        PasswordValidator.__verify_special_char(password)

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

def validate_unique_email(db, email: str):
    '''
    Verifica se o email informado pelo usuário ainda não foi cadastrado

    Parâmetros:
    email (string): string do email cadastrado pelo usuário

    Retorna:
    None

    Levanta:
    HTTPException: se o email já estiver cadastrado
    '''
    from ..database.users import get_user_by_email
    
    user = get_user_by_email(db, email)
    if (user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está cadastrado.",
        )
    
    # Retorna nulo cado a data seja válida
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