import pytest
from fastapi.testclient import TestClient
from backend.main import app, users_db, user_id, expenses_db, expenses_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_dict_before():
    '''
    Limpa o dicionário ("banco de dados" em memória) antes de realizar os testes
    '''
    users_db.clear()
    expenses_db.clear()
    user_id = 0
    expenses_id = 0

###################     TESTES DE USUARIO   ###################

def test_unregistered_user():
    '''
    Testa se o sistema retorna um erro na busca pelos gastos de um usuário não cadastrado
    '''
    response = client.get("/users/99/expenses")
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuário com ID 99 não encontrado."}

###################     TESTES DE GASTOS   ###################

def test_none_expenses():
    '''
    Testa se o sistema retorna uma lista vazia para um usuário cadastrado e sem gastos
    '''
    user_response = client.post("/users", json={"email": "emailtest@teste.com", "password": "SenhaForte@123"})
    user_id = user_response.json()["id"]

    response = client.get(f"/users/{user_id}/expenses")

    assert response.status_code == 200
    assert response.json() == []

def test_with_expenses():
    '''
    Testa se o sistema retorna uma lista com apenas os gastos de um usuário cadastrado
    '''
    # Cria o usuário A
    user_a_res = client.post("/users", json={"email": "emailtestA@teste.com", "password": "SenhaForte@123"})
    user_a = user_a_res.json()

    # Cria o usuário B
    user_b_res = client.post("/users", json={"email": "emailtestB@teste.com", "password": "SenhaForte@123"})
    user_b = user_b_res.json()

    # Cria gastos para o usuário A
    client.post("/expenses", json={"user": user_a, "expense": {"category": "Lazer", "date": "2025-09-02", "value": 150}})
    client.post("/expenses", json={"user": user_a, "expense": {"category": "Alimentação", "date": "2025-07-25", "value": 350}})

    # Cria gastos para o usuário B
    client.post("/expenses", json={"user": user_b, "expense": {"category": "Alimentação", "date": "2025-09-03", "value": 75}})

    # Busca os gatos do usuário A
    response = client.get(f"/users/{user_a['id']}/expenses")

    # Verifica se o retorno está de acordo com o esperado
    assert response.status_code == 200
    expenses_list = response.json()
    assert len(expenses_list) == 2
    assert expenses_list[0]["user_id"] == user_a['id']
    assert expenses_list[1]["user_id"] == user_a['id']