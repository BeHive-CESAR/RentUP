from pydantic import BaseModel
from typing import Optional
from .Role import Role
from infra.entities.users import User

class Users(BaseModel):
    '''Classe para representar Users que vêm da API'''
    nome: Optional[str] = 'Default'
    email: str
    password: str
    role: Optional[Role] = Role.USER

    def to_banco(self):
        '''Metodo que tranforma o objeto Users em um User para o banco de dados'''
        data_insert = User(
                    nome=self.nome,
                    email=self.email,
                    senha=self.password,
                    papel=self.role.name,
                )
        return data_insert