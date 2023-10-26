'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime

class Rent(Base):

    __tablename__ = 'rents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    item_nome = Column(String, nullable=False)
    data_emprestimo = Column(DateTime, nullable=False)
    data_devolucao = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
