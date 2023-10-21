from pydantic import BaseModel
from .Item import Item
from .Role import Role

class Users(BaseModel):
    nome: str
    email: str
    password: str
    role: Role

    def to_banco(self):
        '''Metodo que retorna classe Itens para o banco de dados'''
        data_insert = Users(
                    nome=self.nome,
                    email=self.email,
                    senha=self.password,
                    role=self.role,
                )
        return data_insert