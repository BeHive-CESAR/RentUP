from infra.entities.itens import Itens
from infra.entities.rent import Rent
from infra.configs.connection import DBConnectionHandler
from infra.repository.user_repository import UserRepository
from infra.repository.itens_repository import ItensRepository
from api.entidades.Status import Status
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

    def select_by_user(self, email:str):
        user = UserRepository().select_by_email(email)

        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).filter(Rent.user_id==user.id).all()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro

    def select_by_item(self, item:Itens):
        item = ItensRepository().select_by_item(item)

        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).filter(Rent.item_id==item.id).all()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro

    def select_rent_by_id(self, id:int):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Rent).filter(Rent.id==id).one()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro

    def update(self, rent:Rent, rent2:Rent):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Rent).filter(Rent.id==rent.id).update({
                    'user_id':rent2.user_id,
                    'item_id':rent2.item_id,
                    'data_emprestimo':rent2.data_emprestimo,
                    'data_devolucao':rent2.data_devolucao,
                    'estado':rent2.estado
                })
      
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update_status(self, rent:Rent, status:Status):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Rent).filter(Rent.id==rent.id).update({
                    'estado':status
                })
                db.session.commit()
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

        