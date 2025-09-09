import pytest
from fastapi.testclient import TestClient
from backend.main import app, expenses_db, expenses_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_dict_before_test():
    '''
    Limpa o dicionário ("banco de dados" em memória) antes de realizar os testes
    '''
    global expenses_id
    expenses_db.clear()
    expenses_id = 0

def test_create_mock_user():
    '''
    Cria um usuário dublê para realizar testes de gastos
    '''
    response = client.post(
        "/users",
        json={"email": "emailsucess@gmail.com", "password": "Senha@Forte123"}
    )

    global mock_user
    mock_user = response.json()

###################     TESTES DE USUARIO   ###################

# deve funcionar
def test_registered_user():
    '''
    Testa se o sistema cria um gasto informando um usuário existente
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 201

# devem retornar erro
def test_unregistered_user():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com usuário não cadastrado
    '''
    response = client.post(
        "/expenses",
        json={
            "user": {"id": mock_user["id"]+1, "email": "userUnregistered@email.com"},
            "expense": {
                "category": "Lazer",
                "date": "2025-01-01",
                "value": 403}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 403
    assert response.json() == {"detail": "Usuário não cadastrado. Cadastre-se antes de registrar um gasto."}

def test_none_user():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com usuário None
    '''
    response = client.post(
        "/expenses",
        json={
            "user": None,
            "expense": {
                "category": "Lazer",
                "date": "2025-01-01",
                "value": 422}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 422
    assert response.json() == {"detail": [{"input": None,"loc": ["body", "user"], "msg": "Field required", "type": "missing"}]}

###################     TESTES DE CATEGORIA ###################

# deve funcionar
def test_valid_category():
    '''
    Testa se o sistema cria um gasto informando uma categoria válida
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Alimentação",
                "date": "2025-04-20",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Alimentação"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 201

# devem retornar erro
def test_empty_category():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com categoria vazia
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "",
                "date": "2025-01-01",
                "value": 400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas]."}

def test_none_category():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com categoria None
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": None,
                "date": "2025-01-01",
                "value": 422}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 422
    assert response.json() == {"detail": [{"input": None,"loc": ["body", "expense", "category"], "msg": "Input should be a valid string", "type": "string_type"}]}

def test_invalid_category():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com categoria inválida (qualquer uma fora as definidas)
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Gasolina",
                "date": "2025-01-01",
                "value": 400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Categoria informada é inválida. Informe uma entre [Alimentação; Lazer; Contas]."}

###################     TESTES DE DATA      ###################

# devem funcionar
def test_ISO1_date():
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYYMMDD
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "20250420",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "20250420"
    assert data["value"] == 201

def test_ISO2_date():
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DD
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 201

def test_ISO3_date():
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ss
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20T12:35:20",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20T12:35:20"
    assert data["value"] == 201

def test_ISO4_date():
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ssZ
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20T12:35:20Z",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20T12:35:20Z"
    assert data["value"] == 201

def test_ISO5_date():
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ss+ZZ:zz
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20T12:35:20+02:00",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20T12:35:20+02:00"
    assert data["value"] == 201

def test_ISO6_date():
    '''
    Testa se o sistema cria um gasto informando uma data no formato YYYY-MM-DDTHH:mm:ss-ZZ:zz
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20T12:35:20-03:00",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20T12:35:20-03:00"
    assert data["value"] == 201

# devem retornar erro
def test_empty_date():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data vazia
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "",
                "value": 400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato da data informada é inválido. O formato esperado é YYYY-MM-DD (ou outro no formato ISO)"}

def test_none_date():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com data None
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": None,
                "value": 422}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 422
    assert response.json() == {"detail": [{"input": None,"loc": ["body", "expense", "date"], "msg": "Input should be a valid string", "type": "string_type"}]}

def test_wrong_format_date():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data em formato inválido (qualquer um fora os 6 listados acima)
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "01/01/2025",
                "value": 400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "O formato da data informada é inválido. O formato esperado é YYYY-MM-DD (ou outro no formato ISO)"}

def test_future_date():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando uma data futura
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2026-01-01",
                "value": 400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "A data informada é no futuro. Informe uma data até o dia atual."}

###################     TESTES DE VALOR     ###################

# devem funcionar
def test_positive_integer_value():
    '''
    Testa se o sistema cria um gasto informando um valor inteiro positivo
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 201

def test_float_greater_than_1_value():
    '''
    Testa se o sistema cria um gasto informando um valor decimal maior que um
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 20.1}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 20.1

def test_float_lower_than_1_value():
    '''
    Testa se o sistema cria um gasto informando um valor decimal maior que zero e menor que um
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 0.201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 0.201

def test_large_value():
    '''
    Testa se o sistema cria um gasto informando um valor inteiro muito grande
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 201e100}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["user_id"] == mock_user["id"]
    assert data["category"] == "Lazer"
    assert data["date"] == "2025-04-20"
    assert data["value"] == 201e100

# devem retornar erro
def test_none_value():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com valor None
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": None}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 422
    assert response.json() == {"detail": [{"input": None,"loc": ["body", "expense", "value"], "msg": "Input should be a valid number", "type": "float_type"}]}

def test_zero_value():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor nulo
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-01-01",
                "value": 0}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_negative_integer_value():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor inteiro negativo
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-01-01",
                "value": -400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_float_lower_than_neg1_value():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor decimal entre (-1, 0)
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-01-01",
                "value": -40.0}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

def test_float_greater_than_neg1_value():
    '''
    Testa se o sistema retorna um erro na criação de um gasto informando um valor decimal entre (-inf, -1)
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-01-01",
                "value": -0.400}
            }
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 400
    assert response.json() == {"detail": "Valor informado é inválido. Informe um valor maior ou igual a zero."}

###################     TESTES GERAIS       ###################

# deve funcionar
def test_create_multiple_expenses():
    '''
    Testa se o sistema cria vários gastos corretamente
    '''

    response1 = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Lazer",
                "date": "2025-04-20",
                "value": 201}
            }
    )

    response2 = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": {
                "category": "Contas",
                "date": "2025-04-21",
                "value": 201}
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response1.status_code == 201
    data1 = response1.json()
    assert data1["id"] > 0
    assert data1["user_id"] == mock_user["id"]
    assert data1["category"] == "Lazer"
    assert data1["date"] == "2025-04-20"
    assert data1["value"] == 201

    assert response2.status_code == 201
    data2 = response2.json()
    assert data2["id"] > 0
    assert data2["user_id"] == mock_user["id"]
    assert data2["category"] == "Contas"
    assert data2["date"] == "2025-04-21"
    assert data2["value"] == 201

    assert data2["id"] > data1["id"]

# deve retornar erro
def test_none_expense():
    '''
    Testa se o sistema retorna um erro na criação de um gasto com expense None
    '''
    response = client.post(
        "/expenses",
        json={
            "user": mock_user,
            "expense": None}
    )

    # Verifica se a API retorna o erro corretamente
    assert response.status_code == 422
    assert response.json() == {"detail": [{"input": None,"loc": ["body", "expense"], "msg": "Field required", "type": "missing"}]}
