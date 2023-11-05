from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.mediators.user_mediator import UserMediator

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


def token_verifier(token = Depends(oauth_scheme)):
    uc = UserMediator()
    uc.verify_token(acess_token=token)
    