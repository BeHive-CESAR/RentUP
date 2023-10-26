
from infra.entities.users import User
from infra.entities.itens import Itens
from infra.entities.rent import Rent
from infra.configs.connection import DBConnectionHandler
from sqlalchemy.orm.exc import NoResultFound

class RentRepository:
    def insert(self, rent:Rent):
        with DBConnectionHandler() as db:
            try:
                db.session.add(rent)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro

    def select(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).all()
                return data
            except Exception as erro:
                raise erro

    def select_by_user(self, user:User):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).filter(Rent.user_email==user.email).all()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro

    def select_by_item(self, item:Itens):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).filter(Rent.item_nome==item.nome_item).all()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro

    def select_by_rent(self, rent:Rent):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).filter(Rent.item_nome==rent.item_nome, Rent.user_email==rent.user_email,
                                                     Rent.data_emprestimo==rent.data_emprestimo,Rent.data_devolucao==rent.data_devolucao,
                                                     Rent.estado==rent.estado).one()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro

    def update(self, rent:Rent, rent2:Rent):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Rent).filter(Rent.id==rent.id).update({
                    'id':rent2.id,
                    'user_email':rent2.user_email,
                    'item_nome':rent2.item_nome,
                    'data_emprestimo':rent2.data_emprestimo,
                    'data_devolucao':rent2.data_devolucao,
                    'estado':rent2.estado
                })
      
            except Exception as erro:
                db.session.rollback()
                raise erro

    def delete(self, rent:Rent):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Rent).filter(Rent.id==rent.id).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro

        