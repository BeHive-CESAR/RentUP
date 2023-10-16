from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    '''Classe para representar Itens à API'''
    nome: str
    qntTotal: Optional[int] = None
    qntEmprestar: Optional[int] = None
    qntEmprestados: Optional[int] = None
    qntDanificados: Optional[int] = None
    imagem: Optional[str] = None