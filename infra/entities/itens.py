'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Itens(Base):
    '''Classe responsavel por espelhar um item da tabela itens no banco de dados'''
    __tablename__ = 'itens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_item = Column(String, nullable=False, unique=True)
    qnt_total = Column(Integer, nullable=False)
    qnt_estoque = Column(Integer, nullable=False)
    qnt_emprestar = Column(Integer, nullable=False)
    qnt_emprestados = Column(Integer, nullable=False)
    qnt_danificados = Column(Integer, nullable=False)
    descricao = Column(String, nullable=True)
    imagem = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    rents = relationship('Rent', back_populates='item', cascade='all, delete-orphan')
    category = relationship('Category', back_populates='itens')

    def __repr__(self):
        '''Metodo mágico que é usado para representar o objeto como uma string que pode ser usada para criar um novo objeto com os mesmos valores.'''
        return f'[Item {self.nome_item}, Total {self.qnt_total}, Estoque {self.qnt_estoque}, Emprestados {self.qnt_emprestados}]'
