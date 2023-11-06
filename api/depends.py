from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.mediators.user_mediator import UserMediator


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    return UserMediator().verify_token(auth.credentials)
    