import pytest
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["EXPENSES_DATA_PATH"] = os.path.join(BASE_DIR, "app/utils/data/expenses.json")

from app.main import app, dict_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_users():
    """Reseta dict_db e cria usuários de teste"""
    dict_db.clear()
    dict_db[123] = {"email": "teste123@gmail.com", "password": "123"}
    dict_db[456] = {"email": "teste456@gmail.com", "password": "456"}
    dict_db[789] = {"email": "teste789@gmail.com", "password": "789"}

################### TESTES ###################

def test_user_not_registered():
    response = client.get("/expenses/user/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "User not found"

def test_user_registered():
    response = client.get("/expenses/user/123")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_user_with_no_expenses():
    response = client.get("/expenses/user/789")
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_user_with_expenses():
    response = client.get("/expenses/user/123")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "amount" in item
        assert "category" in item
        assert "date" in item
        assert "description" in item