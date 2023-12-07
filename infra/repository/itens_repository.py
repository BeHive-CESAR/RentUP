'''Através dessa classe iremos realizar o CRUD da tabela itens'''

from infra.configs.connection import DBConnectionHandler
from infra.entities.itens import Itens
from sqlalchemy.orm.exc import NoResultFound

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
    
    def select_item_by_id(self, id:int):
        '''Metodo responsavel por, através do id, buscar o Itens correspondente no banco de dados
        
        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo id para realizar a busca
        '''
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Itens).filter(Itens.id==id).one()
                return data
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
    
    def update_qnt(self, item:Itens):
        '''Metodo resonsavel por editar as quantidade de um Itens no banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo id para realizar a busca
        '''
        with DBConnectionHandler() as db:
            try:
                db.session.query(Itens).filter(Itens.id==item.id).update({
                    'qnt_total': item.qnt_total,
                    'qnt_estoque': item.qnt_estoque,
                    'qnt_emprestar':item.qnt_emprestar,
                    'qnt_emprestados': item.qnt_emprestados,
                    'qnt_danificados': item.qnt_danificados,
                })
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update_infos(self, item:Itens):
        '''Metodo resonsavel por editar as informações de um Itens no banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo id para realizar a busca
        '''
        with DBConnectionHandler() as db:
            try:
                db.session.query(Itens).filter(Itens.id==item.id).update({
                    'nome_item': item.nome_item,
                    'descricao': item.descricao,
                    'imagem': item.imagem,
                    'categoria_id': item.categoria_id,
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
    
    def update_return(self, item_id:int):
        '''Metodo resonsavel por incrementar em 1 o atributo qnt_estoque e decrementar em 1 o qnt_emprestados de um Itens no banco de dados

        Keyword arguments:

        item -- Objeto do tipo Itens que deve possuir o atributo nome_item para realizar a busca e alteração
        '''
        with DBConnectionHandler() as db:
            try:
                data = self.select_item_by_id(item_id)
                db.session.query(Itens).filter(Itens.id==item_id).update(
                    {
                        'qnt_emprestar':data.qnt_emprestar+1,
                        'qnt_emprestados':data.qnt_emprestados-1
                    }
                )
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro        
