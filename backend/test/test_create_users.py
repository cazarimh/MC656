def test_create_user_sucess(test_client):
    '''
    Testa se um usuário é criado com sucesso e o status code retornado é 201
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailsucess@gmail.com", "password": "Senha@Forte123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "emailsucess@gmail.com"
    assert "id" in data["user"]

################### TESTES DE NOME ###################

def test_empty_name(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário sem nome
    '''
    response = test_client.post(
        "/users",
        json={"name": "", "email": "emailteste@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Insira um nome válido."}

################### TESTES DE EMAIL ###################

def test_duplicate_email(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário com email já cadastrado
    '''
    test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "Senha@Forte123"}
    )

    # Tenta criar um segundo usuário com o mesmo email
    response = test_client.post(
        "/users",
        json={"name": "Ciclano Testador", "email": "emailteste@gmail.com", "password": "OutraSenha123@"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Este email já está cadastrado."}

def test_local_part_empty(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com a parte local vazia
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_local_part_contains_special_character(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com a parte local contendo caracteres especiais proibidos
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste*$@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_local_part_contains_space(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com a parte local contendo espaço
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "email teste@gmail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_contains_space(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio contendo espaço
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gm ail.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_contains_underscore(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio contendo underscore
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail_.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_empty(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio vazio
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_domain_contains_special_character(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio contendo caracteres especiais proibidos
    (hífen e ponto são os únicos permitidos)
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail_.com", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_contains_space(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo espaço
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.co m", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_contains_digits(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo dígitos
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com2", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_contains_special_characters(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo caracteres especiais
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com-!", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

def test_tld_length(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário
    com o domínio de nível superior contendo menos de 2 caracteres
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.c", "password": "Senha@Forte123"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato do email é inválido."}

################### TESTES DE PASSWORD ###################

def test_password_length(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha possuindo menos de 8 caracteres
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "Ab1!L()"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos 8 caracteres."}

def test_password_uppercase(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem uma letra maiúscula
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "test123!@"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos uma letra maiúscula."}

def test_password_lowercase(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem uma letra minúscula
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "TEST123!@"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos uma letra minúscula."}

def test_password_digit(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem um dígito
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "TEST!@test"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos um dígito."}

def test_password_special_character(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um
    usuário com a senha sem um caractere especial
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "TEST123test"}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter pelo menos um caractere especial."}