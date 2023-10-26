'''Aqui usamos uma classe para criar nossa tabela e seus respectivos atributos'''

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer
    #user: Users
    #itens: Item
    #rentDate: datetime
    #returnDate: datetime
    #status: Status

class Rent(Base):

    __tablename__ = 'rents'

    user = Column(String, nullable=False)
    itens = Column(String, nullable=False)
    #rentDate = Column(datetime, nullable=False)
    #returnDate = Column(datetime, nullable=False)
    status = Column(String, nullable=False)
