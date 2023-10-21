'''Através dessa classe iremos realizar o CRUD da tabela'''

from infra.entities.users import User
from infra.configs.connection import DBConnectionHandler

class UserRepository:
    '''Essa class é responsavel por conter os metodos que vamos precisar pro CRUD'''
    
    def insert(self, users:User):
        with DBConnectionHandler() as db:
            try:
                db.session.add(users)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).all()
                return data
            except Exception as erro:
                raise erro
    
    def select_by_email(self, user:User):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).filter(User.email==user.email).one()
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
    
    def update(self, user:User, user2:User):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.email==user.email).update({
                    'nome':user2.nome,
                    'email': user2.email,
                    'senha': user2.senha,
                    'papel': user2.papel,
                })
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro