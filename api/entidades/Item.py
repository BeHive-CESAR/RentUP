from pydantic import BaseModel
from typing import Optional
from infra.entities.itens import Itens

class Item(BaseModel):
    '''Classe para representar Itens que vêm da API'''
    nome: str
    qntTotal: Optional[int] = 0
    qntEstoque: Optional[int] = 0
    qntEmprestar: Optional[int] = 0
    qntEmprestados: Optional[int] = 0
    qntDanificados: Optional[int] = 0
    descricao: Optional[int] = None
    imagem: Optional[str] = None

    def to_banco(self):
        '''Metodo que tranforma o objeto Item em um Itens para o banco de dados'''
        data_insert = Itens(
                    nome_item=self.nome.capitalize(),
                    qnt_total=self.qntTotal,
                    qnt_estoque=self.qntEstoque,
                    qnt_emprestar=self.qntEmprestar,
                    qnt_emprestados=self.qntEmprestados,
                    qnt_danificados=self.qntDanificados,
                    descricao=self.descricao
                )
        return data_insert