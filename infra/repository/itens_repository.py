'''Através dessa classe iremos realizar o CRUD da tabela itens'''

from infra.configs.connection import DBConnectionHandler
from infra.entities.itens import Itens
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import aliased
import pandas as pd

class ItensRepository:
    '''Essa class é responsavel por conter os metodos que vamos precisar pro CRUD'''
    def insert(self, item:Itens):
        '''Metodo responsavel por inserir um Itens no banco de dados
        
        Keyword arguments:

        item -- Objeto do tipo Itens a ser inserido
        '''
        with DBConnectionHandler() as db:
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select(self):
        '''Metodo responsavel por buscar todos os Itens no banco de dados'''
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Itens).all()
                return data
            except Exception as erro:
                raise erro
    
    def select_by_item(self, item:Itens):
        '''Metodo responsavel por, através do nome_item, buscar o Itens correspondente no banco de dados
        
        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo nome_item para realizar a busca
        '''
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).one()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro
    
    def delete(self, item:Itens):
        '''Metodo responsavel por deletar um Itens do banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo nome_item para realizar a busca e deleção
        '''
        with DBConnectionHandler() as db:
            try:
                db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update(self, item:Itens, item2:Itens):
        '''Metodo resonsavel por editar um Itens no banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo nome_item para realizar a busca

        item2 -- Objeto do tipo Itens que deverá possuir os novos dados para substituir o registro já existente
        '''
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
    
    def update_rent(self, item:str):
        '''Metodo resonsavel por decrementar em 1 o atributo qnt_estoque e incrementar em 1 o qnt_emprestados de um Itens no banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo nome_item para realizar a busca e alteração
        '''
        with DBConnectionHandler() as db:
            try:
                data = self.select_by_item(Itens(nome_item=item))
                db.session.query(Itens).filter(Itens.nome_item==item).update(
                    {
                        'qnt_emprestar':data.qnt_emprestar-1,
                        'qnt_emprestados':data.qnt_emprestados+1
                    }
                )
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update_return(self, item:Itens):
        '''Metodo resonsavel por incrementar em 1 o atributo qnt_estoque e decrementar em 1 o qnt_emprestados de um Itens no banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo nome_item para realizar a busca e alteração
        '''
        with DBConnectionHandler() as db:
            try:
                data = self.select_by_item(item)
                db.session.query(Itens).filter(Itens.nome_item==item.nome_item.capitalize()).update(
                    {
                        'qnt_emprestar':data.qnt_emprestar+1,
                        'qnt_emprestados':data.qnt_emprestados-1
                    }
                )
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro        
