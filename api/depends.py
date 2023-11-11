from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.mediators.user_mediator import UserMediator


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    '''Metodo responsavel por ler o token passado como parametro no header das requisições é válido
    Deve ser passado como Depends para os endpoints que precisam de autenticação'''
    return UserMediator().verify_token(auth.credentials)

def auth_admin(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    '''Metodo responsavel por ler o token passado como parametro no header das requisições é válido e se o usuario possui permissão de administrador
    Deve ser passado como Depends para os endpoints que precisam de autenticação'''
    return UserMediator().verify_admin(auth.credentials)
    