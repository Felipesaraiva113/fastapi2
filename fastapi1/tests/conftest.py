import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
assert Path.cwd().name == 'fastapi1', 'rode o pytest a partir de fastapi1/'
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env', override=True)
CHAVE = os.getenv('API_KEY', '')
assert CHAVE, 'API_KEY ausente no .env'
from database import Base, get_db
from main import app
from routes import limiter
@pytest.fixture()
def chave():
    return CHAVE
@pytest.fixture()
def cabecalho():
    return {'X-API-Key': CHAVE}
@pytest.fixture()
def cliente(tmp_path):
    motor = create_engine(f'sqlite:///{tmp_path}/teste.db', connect_args={'check_same_thread': False})
    Base.metadata.create_all(bind=motor)
    Sessao = sessionmaker(bind=motor)
    def get_db_teste():
        banco = Sessao()
        try:
            yield banco
        finally:
            banco.close()
    app.dependency_overrides[get_db] = get_db_teste
    limiter._storage.reset()
    with TestClient(app, base_url='http://localhost') as teste:
        yield teste
    app.dependency_overrides.clear()
    limiter._storage.reset()
