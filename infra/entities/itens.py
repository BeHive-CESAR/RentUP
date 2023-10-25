'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer

class Itens(Base):
    '''Classe responsavel por espelhar um item da tabela itens no banco de dados'''
    __tablename__ = 'itens'

    nome_item = Column(String, primary_key=True)
    qnt_total = Column(Integer, nullable=False)
    qnt_estoque = Column(Integer, nullable=False)
    qnt_emprestar = Column(Integer, nullable=False)
    qnt_emprestados = Column(Integer, nullable=False)
    qnt_danificados = Column(Integer, nullable=False)
    descricao = Column(String, nullable=True)

    def __repr__(self):
        '''Metodo mágico que é usado para representar o objeto como uma string que pode ser usada para criar um novo objeto com os mesmos valores.'''
        return f'[Item {self.nome_item}, Total {self.qnt_total}, Estoque {self.qnt_estoque}, Emprestados {self.qnt_emprestados}]'
