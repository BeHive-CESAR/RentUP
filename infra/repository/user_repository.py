'''Através dessa classe iremos realizar o CRUD da tabela'''

from infra.entities.users import User
from infra.configs.connection import DBConnectionHandler

class UserRepository:
    '''Essa class é responsavel por conter os metodos que vamos precisar pro CRUD'''
    
    def insert(self, nome:str, email:str, item:str):
        with DBConnectionHandler() as db:
            try:
                data_insert = User(
                    nome=nome,
                    email=email,
                    item=item.capitalize(),
                    state=True
                )
                db.session.add(data_insert)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select_by_name_email(self, nome:str, email:str):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).filter(User.nome==nome and User.email==email).all()
                return data
            except Exception as erro:
                raise erro
    
    def select_by_item(self, item:str):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).filter(User.item==item.capitalize()).all()
                return data
            except Exception as erro:
                raise erro
    
    def update_state(self, nome:str, email:str, item:str, state:bool):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(
                    User.nome==nome and 
                    User.email == email and
                    User.item == item.capitalize()
                ).update({'state':state})
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def delete_first(self, nome:str, email:str, item:str, state:bool):
        with DBConnectionHandler() as db:
            try:
                id = db.session.query(User).filter(
                    User.nome==nome.capitalize() and
                    User.email==email and
                    User.item==item and
                    User.state==state
                ).first()
                db.session.query(User).filter(User.id==id.id).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def delete_all(self, nome:str, email:str, item:str, state:bool):
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(
                    User.nome==nome.capitalize() and
                    User.email==email and
                    User.item==item and
                    User.state==state
                ).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
