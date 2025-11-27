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
    assert response.json() == {"detail": "Insira um nome."}

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


################### TESTES DE PASSWORD  ###################
# Unidade: Validação de Comprimento de Senha (Comprimento >= 8) (critérios: Análise de Valor Limite (AVL) e Particionamento em Classes de Equivalência (PCE))

# --- AVL: CASO VÁLIDO ---

def test_password_avl_length_min_valido(test_client):
    '''
    [AVL: Limite Válido] Testa a senha com o tamanho mínimo permitido (8 caracteres).
    (Assume: 'A1b@cdef' cumpre as outras regras: maiúsc., minúsc., dígito, especial)
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano AVL", "email": "emailavlminvalido@gmail.com", "password": "A1b@cdef"} # 8 caracteres
    )
    assert response.status_code == 201
    
# --- AVL: CASO INVÁLIDO ---

def test_password_avl_length_min_invalido(test_client):
    '''
    [AVL: Limite Inválido / PCE: Classe Inválida] Testa a senha com o tamanho mais próximo do mínimo que é inválido (7 caracteres).
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Invalido", "email": "emailinvalidolength@gmail.com", "password": "A1b@cde"} # 7 caracteres
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos 8 caracteres."}
    
# --- PCE: CASOS INVÁLIDOS POR REGRAS ADICIONAIS ---

def test_password_pce_sem_maiuscula(test_client):
    '''
    [PCE: Classe Inválida - Sem Maiúscula] Testa se a API retorna erro quando falta uma letra maiúscula.
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailnomaiuscula@gmail.com", "password": "test123!@"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter ao menos uma letra maiúscula."}
    
def test_password_pce_sem_caractere_especial(test_client):
    '''
    [PCE: Classe Inválida - Sem Especial] Testa se a API retorna erro quando falta um caractere especial.
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailnoespecial@gmail.com", "password": "TEST123test"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "A senha deve conter pelo menos um caractere especial."}

def test_duplicate_email(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário com email já cadastrado
    '''
    test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailteste@gmail.com", "password": "Senha@Forte123"}
    )
    response = test_client.post(
        "/users",
        json={"name": "Ciclano Testador", "email": "emailteste@gmail.com", "password": "OutraSenha123@"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Este email já está cadastrado."}

def test_empty_name(test_client):
    '''
    Testa se o sistema retorna um erro na criação de um usuário sem nome
    '''
    response = test_client.post(
        "/users",
        json={"name": "", "email": "emailvaziodenome@gmail.com", "password": "Senha@Forte123"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Insira um nome."}