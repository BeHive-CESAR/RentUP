'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean

class User(Base):
    __tablename__ = 'users'

    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, primary_key=True)
    senha = Column(String, nullable=False)
    papel = Column(String, nullable=False)

    def __repr__(self):
        return f'[Nome: {self.nome}, email: {self.email}, role: {self.papel}]'
