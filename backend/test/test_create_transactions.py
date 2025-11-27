import pytest

@pytest.fixture(scope='function')
def mock_user(test_client):
    '''
    Cria um usuário dublê para realizar testes de transações
    '''
    # garante que o email seja único para cada execução da fixture
    from random import randint
    unique_email = f"emailsucess_{randint(1000, 9999)}@gmail.com"
    
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": unique_email, "password": "Senha@Forte123"}
    )
    return response.json()

################### 	TESTES DE USUARIO 	 ###################
# Unidade: Validação de Usuário (critério: Particionamento em Classes de Equivalência (PCE))

# deve funcionar
def test_registered_user(test_client, mock_user):
    '''
    [PCE: Classe Válida] Testa se o sistema cria um gasto informando um usuário existente.
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Fim de semana no parque"
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Entretenimento"
    assert data["transaction_description"] == "Fim de semana no parque"
    assert "transaction_id" in data

# devem retornar erro
def test_unregistered_user(test_client, mock_user):
    '''
    [PCE: Classe Inválida] Testa se o sistema retorna um erro na criação de um gasto com usuário não cadastrado.
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]+999}/transactions", # ID inexistente
        json={
            "date": "2025-01-01",
            "value": 403,
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Fim de semana no parque"
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 403
    assert response.json() == {"detail": "Usuário não cadastrado."}

################### 	TESTES DE CATEGORIA e TIPO 	 ###################
# Unidade: Validação de Tipos e Categorias fixos (critério: Particionamento em Classes de Equivalência (PCE))

# --- PCE: CASOS VÁLIDOS ---

def test_categoria_pce_receita_valida(test_client, mock_user):
    '''
    [PCE: Classe Válida] Testa o tipo "Receita" com categoria válida ("Investimentos").
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 500,
            "type": "Receita",
            "category": "Investimentos", 
            "description": "Rendimentos"
        }
    )
    assert response.status_code == 201
    assert response.json()["transaction_category"] == "Investimentos"

def test_categoria_pce_despesa_valida(test_client, mock_user):
    '''
    [PCE: Classe Válida] Testa o tipo "Despesa" com categoria válida ("Alimentação").
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 50,
            "type": "Despesa",
            "category": "Alimentação", 
            "description": "Almoço"
        }
    )
    assert response.status_code == 201
    assert response.json()["transaction_category"] == "Alimentação"

# --- PCE: CASOS INVÁLIDOS ---

def test_categoria_pce_tipo_invalido(test_client, mock_user):
    '''
    [PCE: Classe Inválida Tipo] Testa um tipo que não é "Receita" ou "Despesa".
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": 400,
            "type": "Transferencia", # PCE: Tipo Inválido
            "category": "Salário",
            "description": ""
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Tipo informado é inválido. Informe um entre [Receita, Despesa]."}

def test_categoria_pce_categoria_mismatch(test_client, mock_user):
    '''
    [PCE: Classe Inválida Categoria Mismatch] Testa a categoria "Moradia" (Despesa) com o tipo "Receita".
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": 400,
            "type": "Receita",
            "category": "Moradia", # PCE: Categoria Inválida para Receita
            "description": ""
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Categoria informada é inválida. Informe uma entre [Salário, Freelance, Investimentos, Outros]."}


################### 	TESTES DE VALOR 	 ###################
# Unidade: Validação de Valor (critérios: Análise de Valor Limite (AVL) e Particionamento em Classes de Equivalência (PCE))

# --- PCE e AVL: CASOS VÁLIDOS (V > 0) ---

def test_valor_pce_classe_valida_arbitrario(test_client, mock_user):
    '''
    [PCE: Classe Válida] Testa um valor inteiro positivo arbitrário (ex: 400).
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 400, 
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Valor PCE Válido"
        }
    )
    assert response.status_code == 201
    assert response.json()["transaction_value"] == 400

def test_valor_avl_minimo_valido(test_client, mock_user):
    '''
    [AVL: Limite Válido] Testa o valor mais próximo de zero que é permitido (0.01).
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 0.01, # AVL: Mínimo Válido
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Taxa mínima"
        }
    )
    assert response.status_code == 201
    assert response.json()["transaction_value"] == 0.01


# --- PCE & AVL: CASOS INVÁLIDOS (V <= 0) ---

def test_valor_avl_limite_exato_zero(test_client, mock_user):
    '''
    [AVL: Limite Exato / PCE: Classe Inválida I1] Testa o limite exato não permitido (0).
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": 0, # AVL: Limite Exato (Inválido)
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Almoço zero"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_valor_pce_classe_invalida_negativo(test_client, mock_user):
    '''
    [PCE: Classe Inválida I2] Testa um valor negativo arbitrário.
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": -400, # PCE: Exemplo da Classe Inválida I2 (V < 0)
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Almoço negativo"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}


################### 	TESTES DE DATA 	 	###################

def test_ISO2_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DD
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Almoço"
        }
)
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_date"] == "2025-04-20"
    
def test_future_date(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data futura
    '''
    response = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2030-01-01",
            "value": 400,
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Almoço"
        }
)
    assert response.status_code == 400
    assert response.json() == {"detail": "A data informada é no futuro. Informe uma data até o dia atual."}


################### 	TESTES GERAIS 	 	 ###################

def test_create_multiple_transactions(test_client, mock_user):
    '''
    Testa se o sistema cria vários gastos corretamente
    '''
    response1 = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Almoço"
        }
)
    response2 = test_client.post(
        f"/{mock_user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-19",
            "value": 201,
            "type": "Receita",
            "category": "Salário",
            "description": ""
        }
)
    # Verifica se os campos correspondem ao informado
    assert response1.status_code == 201
    data1 = response1.json()
    assert data1["transaction_type"] == "Despesa"

    assert response2.status_code == 201
    data2 = response2.json()
    assert data2["transaction_type"] == "Receita"
    assert data2["transaction_id"] > data1["transaction_id"]