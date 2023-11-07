'''Através dessa classe iremos realizar o CRUD da tabela users'''

from infra.entities.users import User
from infra.configs.connection import DBConnectionHandler
from sqlalchemy.orm.exc import NoResultFound

class UserRepository:
    '''Essa class é responsavel por conter os metodos que vamos precisar pro CRUD'''
    
    def insert(self, users:User):
        '''Metodo responsavel por inserir um User no banco de dados
        
        Keyword arguments:

        users -- Objeto do tipo User a ser inserido
        '''
        with DBConnectionHandler() as db:
            try:
                db.session.add(users)
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def select(self):
        '''Metodo responsavel por buscar todos os User no banco de dados'''
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).all()
                return data
            except Exception as erro:
                raise erro
    
    def select_by_email(self, email:str):
        '''Metodo responsavel por, através do email, buscar o User correspondente no banco de dados
        
        Keyword arguments:

        user -- Objeto do tipo User que deve possuir o atributo email para realizar a busca
        '''
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(User).filter(User.email==email).one()
                return data
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro
    
    def delete(self, users:User):
        '''Metodo responsavel por deletar um User do banco de dados

        Keyword arguments:
        
        users -- Objeto do tipo User que deve possuir o atributo email para realizar a busca e deleção
        '''
        with DBConnectionHandler() as db:
            try:
                db.session.query(User).filter(User.email==users.email).delete()
                db.session.commit()
            except Exception as erro:
                db.session.rollback()
                raise erro
    
    def update(self, user:User, user2:User):
        '''Metodo resonsavel por editar um User no banco de dados

        Keyword arguments:

        user -- Objeto do tipo User que deve possuir o atributo email para realizar a busca
        user2 -- Objeto do tipo User que deverá possuir os novos dados para substituir o registro já existente
        '''
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
            
    def select_by_name(self, nome:str):
        with DBConnectionHandler() as db:
            try:
                return db.session.query(User).filter(User.nome==nome).all()
            except NoResultFound:
                return None
            except Exception as erro:
                raise erro       
