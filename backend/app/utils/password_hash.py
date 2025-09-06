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