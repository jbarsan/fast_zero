from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User

"""
def test_create_user(session):
    new_user = User(
        username="alice",
        password="secret",
        email="test@test.com",
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(
        select(User).where(User.username == "alice")
    )

    assert user.username == 'alice'
"""

"""
session.add(new_user) O método .add da sessão, adiciona o registro a sessão.
O dado fica em um estado transiente. Ele não foi adicionado ao banco de dados
ainda. Mas já está reservado na sessão. Ele é uma aplicação do padrão de
projeto Unidade de trabalho.

session.commit() No momento em que existem dados transientes na sessão e
queremos "performar" efetivamente as ações no banco de dados. Usamos o método
.commit.

O método .scalar é usado para performar buscas no banco (queries). Ele pega o
primeiro resultado da busca e faz uma operação de converter o resultado do
banco de dados em um Objeto criado pelo SQLAlchemy, nesse caso, caso encontre
um resultado, ele irá converter na classe User. A função de select é uma função
de busca de dados no banco. Nesse caso estamos procurando em todos os Users
onde (where) o nome é igual a "alice".
"""


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
        username="alice",
        password="secret",
        email="test@test.com",
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(
        select(User).where(User.username == "alice")
    )

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'test@test.com',
        'created_at': time,
        'updated_at': time, # Exercício
    }


"""
with mock_db_time(model=User) as time: Inicia o gerenciador de contexto
mock_db_time usando o modelo User como base.

asdict(user) Converte o user em um dicionário para simplificar a validação no
teste.

'created_at': time Usa o time gerado por mock_db_time para validar o campo
created_at.

"""
