from pydantic import BaseModel
from typing import Optional

class CategoriaName(BaseModel):
    nome: str

class Categoria(CategoriaName):
    descricao: Optional[str] = ''

class BaseItem(BaseModel):
    nome: str

class ItemDescription(BaseItem):
    descricao: Optional[str] = ''
    imagem: Optional[str] = ''
    categoria: str = ''

class ItemQnt(BaseItem):
    '''Classe para representar Itens que vêm da API'''
    qntEstoque: int = 0
    qntEmprestar: int = 0
    qntEmprestados: int = 0
    qntDanificados: int = 0

class Item(ItemDescription, ItemQnt):
    pass
