from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


"""
create_engine('sqlite:///:memory:'): cria um mecanismo de banco de dados SQLite
em memória usando SQLAlchemy. Este mecanismo será usado para criar uma sessão
de banco de dados para nossos testes.

table_registry.metadata.create_all(engine): cria todas as tabelas no banco de
dados de teste antes de cada teste que usa a fixture session.

Session(engine): cria uma sessão Session para que os testes possam se comunicar
com o banco de dados via engine.

yield session: fornece uma instância de Session que será injetada em cada teste
que solicita a fixture session. Essa sessão será usada para interagir com o
banco de dados de teste.

table_registry.metadata.drop_all(engine): após cada teste que usa a fixture
session, todas as tabelas do banco de dados de teste são eliminadas, garantindo
que cada teste seja executado contra um banco de dados limpo.
"""


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"): # Exercício
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


"""
O decorador @contextmanager cria um gerenciador de contexto para que a função
_mock_db_time seja usada com um bloco with.

Todos os parâmetros após * devem ser chamados de forma nomeada, para ficarem
explícitos na função. Ou seja mock_db_time(model=User). Os parâmetros não podem
ser chamados de forma posicional _mock_db_time(User), isso acarretará em um
erro.

def fake_time_hook() Função para alterar alterar o método created_at do objeto
de target.

event.listen adiciona um evento relação a um model que será passado a função.
Esse evento é o before_insert, ele executará uma função (hook) antes de inserir
o registro no banco de dados. O hook é a função fake_time_hook.

yield time Retorna o datetime na abertura do gerenciamento de contexto.

event.remove() Após o final do gerenciamento de contexto o hook dos eventos é
removido.
"""


@pytest.fixture
def mock_db_time():
    return _mock_db_time
