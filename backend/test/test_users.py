import pytest
from fastapi.testclient import TestClient
from backend.main import app, dict_db, user_id as main_user_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_dict_before_test():
    '''
    Limpa o dicionário ("banco de dados" em memória) antes de realizar os testes
    '''
    global main_user_id
    dict_db.clear()
    main_user_id = 0

def test_create_user_sucess():
    '''
    Testa se um usuário é criado com sucesso e o status code retornado é 201
    '''
    response = client.post(
        "/users",
        json={"email": "emailsucess@gmail.com", "password": "Senha@Forte123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "emailsucess@gmail.com"
    assert "id" in data
    assert "password" not in data

################### TESTES DE EMAIL ###################

def test_duplicate_email():
    '''
    Testa se o sistema retorna um erro na criação de um usuário com email já cadastrado
    '''
    client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "Senha@Forte123"}
    )

    # Tenta criar um segundo usuário com o mesmo email
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "OutraSenha123@"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Este email já está cadastrado."}

def test_local_part_empty():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com a parte local vazia
    '''
    response = client.post(
        "/users",
        json={"email": "@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_local_part_contains_special_character():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com a parte local contendo caracteres especiais proibidos
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste*$@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_local_part_contains_space():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com a parte local contendo espaço
    '''
    response = client.post(
        "/users",
        json={"email": "email teste@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_contains_space():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio contendo espaço
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gm ail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_contains_underscore():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio contendo underscore
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail_.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_empty():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio vazio
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_contains_special_character():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio contendo caracteres especiais proibidos
    (hífen e ponto são os únicos permitidos)
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail_.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_contains_space():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo espaço
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.co m", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_contains_digits():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo dígitos
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com2", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_contains_special_characters():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo caracteres especiais
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com-!", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_length():
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo menos de 2 caracteres
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.c", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

################### TESTES DE PASSWORD ###################

def test_password_length():
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha possuindo menos de 8 caracteres
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "Ab1!L()"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos 8 caracteres."}

def test_password_uppercase():
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem uma letra maiúscula
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "test123!@"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos uma letra maiúscula."}

def test_password_lowercase():
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem uma letra minúscula
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "TEST123!@"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos uma letra minúscula."}

def test_password_digit():
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem um dígito
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "TEST!@test"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos um dígito."}

def test_password_special_character():
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem um caractere especial
    '''
    response = client.post(
        "/users",
        json={"email": "emailteste@gmail.com", "password": "TEST123test"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter pelo menos um caractere especial."}