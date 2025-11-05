import pytest

@pytest.fixture(scope='function')
def mock_user_and_transactions(test_client):
    '''
    Cria um usuário dublê com transações para realizar testes de transações
    '''
    user_response = test_client.post(
        "/users",
        json={"name": "Fulano Testador", "email": "emailsucess@gmail.com", "password": "Senha@Forte123"}
    )

    user = user_response.json()

    test_client.post(
        f"/{user["user_id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Lazer",
            "description": "Fim de semana no parque"
            }
    )

    test_client.post(
        f"/{user["user_id"]}/transactions",
        json={
            "date": "2025-04-21",
            "value": 201,
            "type": "Despesa",
            "category": "Alimentação",
            "description": "Fim de semana no parque"
            }
    )

    test_client.post(
        f"/{user["user_id"]}/transactions",
        json={
            "date": "2025-04-22",
            "value": 201,
            "type": "Receita",
            "category": "Contas",
            "description": "Salário"
            }
    )

    return user

###################     TESTES DE USUARIO   ###################

def test_unregistered_user(test_client, mock_user_and_transactions):
    '''
    Testa se o sistema retorna um erro na busca pelas transações de um usuário não cadastrado
    '''
    response = test_client.get(f"/{mock_user_and_transactions["user_id"]+1}/transactions")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Usuário com ID {mock_user_and_transactions["user_id"]+1} não encontrado."}

###################     TESTES DE TRANSAÇÕES   ###################

def test_no_transactions(test_client, mock_user_and_transactions):
    '''
    Testa se o sistema retorna uma lista vazia para um usuário cadastrado e sem transações
    '''
    user_response = test_client.post("/users", json={"name": "Ciclano Testador", "email": "emailsucess@teste.com", "password": "Senha@Forte123"})
    user = user_response.json()

    response = test_client.get(f"/{user["user_id"]}/transactions")

    assert response.status_code == 200
    assert response.json() == []

def test_with_transactions(test_client, mock_user_and_transactions):
    '''
    Testa se o sistema retorna uma lista com apenas as transações de um usuário cadastrado
    '''
    # Cria o usuário A
    user_A = test_client.post("/users", json={"name": "Maria", "email": "emailtestA@teste.com", "password": "SenhaForte@123"}).json()

    # Cria o usuário B
    user_B = test_client.post("/users", json={"name": "Henrique", "email": "emailtestB@teste.com", "password": "SenhaForte@123"}).json()

    # Cria transações para o usuário A
    test_client.post(f"/{user_A["user_id"]}/transactions", json={"date": "2025-09-02", "value": 150, "type": "Despesa", "category": "Lazer", "description": ""})

    # Cria transações para o usuário B
    test_client.post(f"/{user_B["user_id"]}/transactions", json={"date": "2025-09-03", "value": 75, "type": "Despesa", "category": "Alimentação", "description": "Almoço"})

    # Cria transações para o usuário A
    test_client.post(f"/{user_A["user_id"]}/transactions", json={"date": "2025-07-25", "value": 350, "type": "Despesa", "category": "Alimentação", "description": "Janta"})

    # Busca as transações do usuários
    response_mock = test_client.get(f"/{mock_user_and_transactions["user_id"]}/transactions")
    response_A = test_client.get(f"/{user_A["user_id"]}/transactions")
    response_B = test_client.get(f"/{user_B["user_id"]}/transactions")

    # Verifica se o retorno está de acordo com o esperado
    assert response_mock.status_code == 200
    transactions_list_mock = response_mock.json()
    assert len(transactions_list_mock) == 3
    for transaction in transactions_list_mock:
        assert transaction["user_id"] == mock_user_and_transactions["user_id"]

    assert response_A.status_code == 200
    transactions_list_A = response_A.json()
    assert len(transactions_list_A) == 2
    for transaction in transactions_list_A:
        assert transaction["user_id"] == user_A["user_id"]

    assert response_B.status_code == 200
    transactions_list_B = response_B.json()
    assert len(transactions_list_B) == 1
    for transaction in transactions_list_B:
        assert transaction["user_id"] == user_B["user_id"]
