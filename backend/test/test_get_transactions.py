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
        f"/{user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-20",
            "value": 201,
            "type": "Despesa",
            "category": "Entretenimento",
            "description": "Fim de semana no parque"
            }
    )

    test_client.post(
        f"/{user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-21",
            "value": 201,
            "type": "Despesa",
            "category": "Alimentação",
            "description": "Fim de semana no parque"
            }
    )

    test_client.post(
        f"/{user["user"]["id"]}/transactions",
        json={
            "date": "2025-04-22",
            "value": 201,
            "type": "Receita",
            "category": "Salário",
            "description": ""
            }
    )

    return user

###################     TESTES DE USUARIO   ###################

def test_unregistered_user(test_client, mock_user_and_transactions):
    '''
    Testa se o sistema retorna um erro na busca pelas transações de um usuário não cadastrado
    '''
    response = test_client.get(f"/{mock_user_and_transactions["user"]["id"]+1}/transactions")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Usuário com ID {mock_user_and_transactions["user"]["id"]+1} não encontrado."}

###################     TESTES DE TRANSAÇÕES   ###################

def test_no_transactions(test_client, mock_user_and_transactions):
    '''
    Testa se o sistema retorna uma lista vazia para um usuário cadastrado e sem transações
    '''
    user_response = test_client.post("/users", json={"name": "Ciclano Testador", "email": "emailsucess@teste.com", "password": "Senha@Forte123"})
    user = user_response.json()

    response = test_client.get(f"/{user["user"]["id"]}/transactions")

    assert response.status_code == 200
    assert response.json() == []

def test_with_transactions(test_client, mock_user_and_transactions):
    '''
    Testa se o sistema retorna uma lista com apenas as transações de um usuário cadastrado
    '''

    user_A = test_client.post(
        "/users",
        json={"name": "Maria",
              "email": "emailtestA@teste.com",
              "password": "SenhaForte@123"
              }
    ).json()

    user_B = test_client.post(
        "/users",
        json={"name": "Henrique",
              "email": "emailtestB@teste.com",
              "password": "SenhaForte@123"
              }
    ).json()

    test_client.post(
        f"/{user_A["user"]["id"]}/transactions",
        json={"date": "2025-09-02",
              "value": 150,
              "type": "Despesa",
              "category": "Entretenimento",
              "description": "Cinema"
              }
    )

    test_client.post(
        f"/{user_B["user"]["id"]}/transactions",
        json={"date": "2025-09-03",
              "value": 75,
              "type": "Despesa",
              "category": "Alimentação",
              "description": "Almoço"
              }
    )

    test_client.post(
        f"/{user_A["user"]["id"]}/transactions",
        json={"date": "2025-07-25",
              "value": 350,
              "type": "Receita",
              "category": "Salário",
              "description": ""
              }
    )

    response_mock = test_client.get(f"/{mock_user_and_transactions["user"]["id"]}/transactions")
    response_A = test_client.get(f"/{user_A["user"]["id"]}/transactions")
    response_B = test_client.get(f"/{user_B["user"]["id"]}/transactions")

    def assert_test(response, num_transactions, owner):
        assert response.status_code == 200
        transactions_list = response.json()
        assert len(transactions_list) == num_transactions
        for transaction in transactions_list:
            assert transaction["user_id"] == owner["user"]["id"]
            assert transaction is not None

    assert_test(response_mock, 3, mock_user_and_transactions)
    assert_test(response_A, 2, user_A)
    assert_test(response_B, 1, user_B)
