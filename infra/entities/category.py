from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(Text, nullable=True)
    itens = relationship('Itens', lazy='subquery', back_populates='category', cascade='all, delete-orphan')