from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    '''
    Gera um hash para a senha fornecida.

    Parâmetros:
    password (str): string com a senha original.

    Retorna:
    str: hash da senha    
    '''
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Verifica se a senha em texto puro bate com o hash salvo.

    Parâmetros:
    plain_password (str): A senha que o usuário digitou.
    hashed_password (str): O hash que está salvo no banco.

    Retorna:
    bool: True se a senha bater, False caso contrário.
    '''
    return password_context.verify(plain_password, hashed_password)