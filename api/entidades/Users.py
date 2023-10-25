from pydantic import BaseModel
from .Role import Role
from infra.entities.users import User

class Users(BaseModel):
    '''Classe para representar Users que vêm da API'''
    nome: str
    email: str
    password: str
    role: Role

    def to_banco(self):
        '''Metodo que tranforma o objeto Users em um User para o banco de dados'''
        data_insert = User(
                    nome=self.nome,
                    email=self.email,
                    senha=self.password,
                    papel=self.role.name,
                )
        return data_insert