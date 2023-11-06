from pydantic import BaseModel
from typing import Optional
from .Role import Role
from infra.entities.users import User


class UserAuth(BaseModel):
    email: str
    password: str

class Users(UserAuth):
    '''Classe para representar Users que vêm da API'''
    nome: str 
    contato: str
    role: Role = Role.USER

    def to_banco(self):
        '''Metodo que tranforma o objeto Users em um User para o banco de dados'''
        data_insert = User(
                    nome=self.nome,
                    email=self.email,
                    senha=self.password,
                    contato=self.contato,
                    papel=self.role.name
                )
        
        return data_insert

