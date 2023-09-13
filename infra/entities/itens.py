'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Itens(Base):
    __tablename__ = 'itens'

    nome_item = Column(String, primary_key=True)
    qnt_total = Column(Integer, nullable=False)
    qnt_estoque = Column(Integer, nullable=False)
    qnt_emprestados = Column(Integer, nullable=False)
    qnt_danificados = Column(Integer, nullable=False)
    emprestimos = relationship('User', backref='users', lazy='subquery')

    def __repr__(self):
        return f'[Item {self.nome_item}, Total {self.qnt_total}, Estoque {self.qnt_estoque}, Emprestados {self.qnt_emprestados}]'
