'''Através dessa classe iremos realizar o CRUD da tabela'''

from infra.entities.users import User
from infra.configs.connection import DBConnectionHandler

class UserRepository:
    '''Essa class é responsavel por conter os metodos que vamos precisar pro CRUD'''
    
    def insert(self, users:User):
        with DBConnectionHandler() as db:
            try:
                db.session.add(User)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select_by_name_email(self, User:str, email:str):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).filter(User.nome and User.email==email).all()
                return data
            except Exception as erro:
                raise erro
    
    def delete(self, users:User):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.email==users.email).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update(self, user:User):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.nome_item==item.nome_item.capitalize()).update({
                    'nome_usuario':user.nome,
                    'email': user.email,
                    'senha': user.senha,
                    'role': user.role,
                })
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro