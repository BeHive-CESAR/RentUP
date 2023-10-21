from pydantic import BaseModel
from .Role import Role
from infra.entities.users import User

class Users(BaseModel):
    nome: str
    email: str
    password: str
    role: Role

    def to_banco(self):
        '''Metodo que retorna classe Itens para o banco de dados'''
        data_insert = User(
                    nome=self.nome,
                    email=self.email,
                    senha=self.password,
                    papel=self.role.name,
                )
        return data_insert