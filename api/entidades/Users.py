from pydantic import BaseModel
from .Item import Item

class Users(BaseModel):
    '''Classe para representar Usuarios à API'''
    nome: str
    email: str
    itens: Item
