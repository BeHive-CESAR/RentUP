'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class User(Base):
    '''Classe responsavel por espelhar um user da tabela users no banco de dados'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    contato = Column(String, nullable=False, unique=True)
    papel = Column(String, nullable=False)
    rents = relationship('Rent', back_populates='users', cascade='all, delete-orphan')

    def __repr__(self):
        '''Metodo mágico que é usado para representar o objeto como uma string que pode ser usada para criar um novo objeto com os mesmos valores.'''
        return f'[Nome: {self.nome}, email: {self.email}, role: {self.papel}]'
