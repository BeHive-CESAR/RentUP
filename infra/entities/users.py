'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    item = Column(String, ForeignKey('itens.nome_item'))
    state = Column(Boolean, nullable=False)

    def __repr__(self):
        return f'[Nome: {self.nome}, item emprestado: {self.item}, Estado: {self.state}]'
