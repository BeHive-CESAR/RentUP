from pydantic import BaseModel, EmailStr
from .Role import Role


class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserData(UserAuth):
    nome: str 
    contato: str

class Users(UserData):
    '''Classe para representar Users que vêm da API'''
    role: Role = Role.USER

