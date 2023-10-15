from pydantic import BaseModel

class Item(BaseModel):
    '''Classe para representar Itens à API'''
    nome: str
    qntTotal: int
    qntEmprestar: int
    qntEmprestados: int
    qntDanificados: int
    imagem: str