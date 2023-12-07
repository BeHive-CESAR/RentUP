from infra.configs.connection import DBConnectionHandler
from infra.entities.category import Category
from sqlalchemy.orm.exc import NoResultFound

class CategoryRepository:
    def insert(self, category:Category):
        with DBConnectionHandler() as db:
            category.nome = category.nome.capitalize()
            try:
                db.session.add(category)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Category).all()
                return data
            except Exception as erro:
                raise erro
    
    def update(self, category:Category):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Category).filter(Category.id==category.id).update({
                    'nome': category.nome,
                    'descricao': category.descricao
                })
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro

    def select_by_name(self, category:Category):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Category).filter(Category.nome==category.nome.capitalize()).one()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro