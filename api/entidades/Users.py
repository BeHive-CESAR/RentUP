from pydantic import BaseModel, EmailStr
from .Role import Role


class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserCreation(UserAuth):
    nome: str 
    contato: str

class Users(UserCreation):
    '''Classe para representar Users que vêm da API'''
    role: Role = Role.USER

