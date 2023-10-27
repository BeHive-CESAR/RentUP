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
    estado = Column(String, nullable=False)

    def __repr__(self):
        '''Metodo mágico que é usado para representar o objeto como uma string que pode ser usada para criar um novo objeto com os mesmos valores.'''
        return f'[Id: {self.id}, usuário: {self.user_email}, item: {self.item_nome}, data emprestimo: {self.data_emprestimo},\
 data devolução: {self.data_devolucao}, estado: {self.estado}]'

