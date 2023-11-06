'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String

class User(Base):
    '''Classe responsavel por espelhar um user da tabela users no banco de dados'''
    __tablename__ = 'users'

    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, primary_key=True)
    senha = Column(String, nullable=False)
    contato = Column(String, nullable=False)
    papel = Column(String, nullable=False)

    def __repr__(self):
        '''Metodo mágico que é usado para representar o objeto como uma string que pode ser usada para criar um novo objeto com os mesmos valores.'''
        return f'[Nome: {self.nome}, email: {self.email}, role: {self.papel}]'
