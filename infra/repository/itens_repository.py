'''Através dessa classe iremos realizar o CRUD da tabela'''

from infra.configs.connection import DBConnectionHandler
from infra.entities.itens import Itens
from sqlalchemy.orm.exc import NoResultFound
import pandas as pd

class ItensRepository:
    '''Essa class é responsavel por conter os metodos que vamos precisar pro CRUD'''
    def insert(self, item:Itens):
        with DBConnectionHandler() as db:
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Itens).all()
                return data
            except Exception as erro:
                raise erro
    
    def select_by_item(self, item:Itens):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).one()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro
    
    def delete(self, item:Itens):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update(self, item:Itens, item2:Itens):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).update({
                    'nome_item':item2.nome_item,
                    'qnt_total': item2.qnt_total,
                    'qnt_estoque': item2.qnt_estoque,
                    'qnt_emprestar':item2.qnt_emprestar,
                    'qnt_emprestados': item2.qnt_emprestados,
                    'qnt_danificados': item2.qnt_danificados,
                    'descricao': item2.descricao
                })
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update_loan(self, item:Itens):
        with DBConnectionHandler() as db:
            try:
                data = self.select_by_item(item)
                db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).update(
                    {
                        'qnt_estoque':data.qnt_estoque-1,
                        'qnt_emprestados':data.qnt_emprestados+1
                    }
                )
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update_return(self, item:Itens):
        with DBConnectionHandler() as db:
            try:
                data = self.select_by_item(item)
                db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).update(
                    {
                        'qnt_estoque':data.qnt_estoque+1,
                        'qnt_emprestados':data.qnt_emprestados-1
                    }
                )
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def insert_excel(self, excel:str):
        try:
            data_excel = pd.read_excel(excel)
            data_excel = data_excel.iloc

            for data in data_excel:
                data = data.to_list()
                if self.select_by_item(data[0]):
                    self.update(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]))
                else:
                    self.insert(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]))
        except Exception as erro:
            raise erro
    
    def export_excel(self, excel_path:str='itens_bd.xlsx'):
        with DBConnectionHandler() as db:
            try:
                sql_consult = 'SELECT * FROM itens'
                data = pd.read_sql_query(sql_consult, db.get_engine())
                data.to_excel(excel_path, index=False)
            except Exception as erro:
                raise erro
        
