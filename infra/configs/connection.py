from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

class DBConnectionHandler:
    '''Classe que permitirá a conexão com o banco de dados'''

    def __init__(self):
        '''Metodo inicial que define o nosso "link" de conexão com o banco especificado'''

        self.__connection_string = config('CONNECT')
        self.__engine = self.__create_database_egine()
        self.session = None

    def __create_database_egine(self):
        '''Metedo usado para criar a conexão do nosso código com o banco'''
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        '''Caso precise, podemos ver nossa engine que é a nossa conexão com o banco'''
        return self.__engine

    def __enter__(self):
        '''Método mágico que é executado ao entrar em um bloco with'''
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Método mágico que é executado ao sair de um bloco with'''
        self.session.close()
