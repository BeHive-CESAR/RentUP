from pydantic import BaseModel
from typing import Optional
from infra.entities.itens import Itens


class BaseItem(BaseModel):
    nome: str

class Item(BaseItem):
    '''Classe para representar Itens que vêm da API'''
    qntEstoque: int = 0
    qntEmprestar: int = 0
    qntEmprestados: int = 0
    qntDanificados: int = 0
    descricao: Optional[str] = ''
    imagem: Optional[str] = ''

class ReturnItem(Item):
    qntTotal: int = 0
