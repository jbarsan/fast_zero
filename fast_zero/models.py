from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

"""
# Mapped refere-se a um atributo Python que é associado (ou mapeado) a uma
# coluna específica em uma tabela de banco de dados.

# Mapped permite ao SQLAlchemy realizar a conversão entre os tipos de dados
# Python e os tipos de dados do banco de dados, além de oferecer uma interface
# Pythonica para a interação entre eles.

# Cada classe que é registrada pelo objeto registry é automaticamente mapeada
# para uma tabela no banco de dados.
"""
table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'  # nome que a tabela terá no banco de dados

    # id: Mapped[int] indica que este atributo é um inteiro que será mapeado
    # para uma coluna correspondente em uma tabela de banco de dados.
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column( # Exercício
        init=False, server_default=func.now(), onupdate=func.now()
    )


"""
init=False diz que, quando o objeto for instanciado, esse parâmetro não deve
ser passado.

primary_key=True diz que o campo id é a chave primária dessa tabela.

unique=True diz que esse campo não deve se repetir na tabela. Por exemplo, se
tivermos um username "dunossauro", não podemos ter outro com o mesmo valor.

server_default=func.now() diz que, quando a classe for instanciada, o resultado
de func.now() será o valor atribuído a esse atributo. No caso, a data e hora em
que ele foi instanciado.
"""
