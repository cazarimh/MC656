import pytest
from fastapi.testclient import TestClient
from backend.main import app, get_db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.database.config import Base

DATABASE_URL = 'sqlite:///./backend/test/test.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    '''
    Cria um banco de dados de teste antes de realizar os testes
    '''

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def test_db_session():
    '''
    Cria uma conexão limpa com o banco de dados de teste antes de realizar os testes
    '''

    db = TestSessionLocal()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f'DELETE FROM {table.name}'))
        yield db
    finally:
        db.close()

@pytest.fixture(scope='function')
def test_client(test_db_session):
    '''
    Sobrescreve a dependência da criação da sessão do banco de dados
    '''

    def override_get_db():
        yield test_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()