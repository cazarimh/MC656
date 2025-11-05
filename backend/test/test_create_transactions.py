import pytest

@pytest.fixture(scope='function')
def mock_user(test_client):
    '''
    Cria um usuário dublê para realizar testes de transações
    '''
    response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailsucess@gmail.com", "password": "Senha@Forte123"}
    )

    return response.json()

###################     TESTES DE USUARIO   ###################

# deve funcionar
def test_registered_user(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando um usuário existente
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Fim de semana no parque"
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Fim de semana no parque"
    assert "transaction_id" in data

# devem retornar erro
def test_unregistered_user(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto com usuário não cadastrado
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]+1}/transactions",
        json={
            "date": "2025-01-01",
            "value": 403,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Fim de semana no parque"
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 403
    assert response.json() == {"detail": "Usuário não cadastrado. Cadastre-se antes de registrar um gasto."}

###################     TESTES DE CATEGORIA ###################

# deve funcionar
def test_valid_category(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma categoria válida
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Alimentação",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Alimentação"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

# devem retornar erro
def test_empty_category(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto com categoria vazia
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": 400,
            "type": "Receita",
            "category": "",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas]."}

def test_invalid_category(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto com categoria inválida (qualquer uma fora as definidas)
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": 400,
            "type": "Receita",
            "category": "Gasolina",
            "description": ""
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas]."}

###################     TESTES DE DATA      ###################

# devem funcionar
def test_ISO1_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYYMMDD
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "20250420",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Parque"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Parque"
    assert "transaction_id" in data

def test_ISO2_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DD
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_ISO3_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ss
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20T12:35:20",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_ISO4_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ssZ
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20T12:35:20Z",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_ISO5_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ss+ZZ:zz
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20T12:35:20+02:00",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_ISO6_date(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ss-ZZ:zz
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20T12:35:20-03:00",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

# devem retornar erro
def test_empty_date(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data vazia
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "",
            "value": 400,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato da data informada é inválido. O formato esperado é YYYY-MM-DD (ou outro no formato ISO)"}

def test_wrong_format_date(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data em formato inválido (qualquer um fora os 6 listados acima)
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "01/01/2025",
            "value": 400,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato da data informada é inválido. O formato esperado é YYYY-MM-DD (ou outro no formato ISO)"}

def test_future_date(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data futura
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2030-01-01",
            "value": 400,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A data informada é no futuro. Informe uma data até o dia atual."}

###################     TESTES DE VALOR     ###################

# devem funcionar
def test_positive_integer_value(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando um valor inteiro positivo
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_float_greater_than_1_value(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando um valor decimal maior que um
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 20.1,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 20.1
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_float_lower_than_1_value(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando um valor decimal maior que zero e menor que um
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 0.201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 0.201
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

def test_large_value(test_client, mock_user):
    '''
    Testa se o sistema cria um gasto informando um valor inteiro muito grande
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201e100,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == mock_user["user_id"]
    assert data["transaction_date"] == "2025-04-20"
    assert data["transaction_value"] == 201e100
    assert data["transaction_type"] == "Despesa"
    assert data["transaction_category"] == "Lazer"
    assert data["transaction_description"] == "Almoço"
    assert "transaction_id" in data

# devem retornar erro
def test_zero_value(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor nulo
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": 0,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_negative_integer_value(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor inteiro negativo
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": -400,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_float_lower_than_neg1_value(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor decimal entre (-1, 0)
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": -40.0,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_float_greater_than_neg1_value(test_client, mock_user):
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor decimal entre (-inf, -1)
    '''
    response = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-01-01",
            "value": -0.400,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

###################     TESTES GERAIS       ###################

# deve funcionar
def test_create_multiple_transactions(test_client, mock_user):
    '''
    Testa se o sistema cria vários gastos corretamente
    '''

    response1 = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Almoço"
        }
)
    response2 = test_client.post(
        f"/{mock_user["user_id"]}/transactions",
        json={
            "date": "2025-04-19",
            "value": 201,
            "type": "Receita",
            "category": "Alimentação",
            "description": "Marmita"
        }
)
    # Verifica se os campos correspondem ao informado
    assert response1.status_code == 201
    data1 = response1.json()
    assert data1["user_id"] == mock_user["user_id"]
    assert data1["transaction_date"] == "2025-04-20"
    assert data1["transaction_value"] == 201
    assert data1["transaction_type"] == "Despesa"
    assert data1["transaction_category"] == "Lazer"
    assert data1["transaction_description"] == "Almoço"
    assert "transaction_id" in data1

    assert response2.status_code == 201
    data2 = response2.json()
    assert data2["user_id"] == mock_user["user_id"]
    assert data2["transaction_date"] == "2025-04-19"
    assert data2["transaction_value"] == 201
    assert data2["transaction_type"] == "Receita"
    assert data2["transaction_category"] == "Alimentação"
    assert data2["transaction_description"] == "Marmita"
    assert "transaction_id" in data2

    assert data2["transaction_id"] > data1["transaction_id"]
