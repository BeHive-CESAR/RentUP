from api.entidades.Rent import Rent
from infra.repository.rent_repository import RentRepository
from infra.repository.itens_repository import ItensRepository, Itens
from api.entidades.Users import User
from .item_mediator import ItemMediator, Item
from datetime import datetime

class RentMediator:
    def __init__(self):
        self.repo=RentRepository()
        self.repoItens=ItensRepository()
        self.medItens=ItemMediator()

    def __validate(self, rent:Rent):
        ''' Metodo reponsável por validar se o Rent pode ser realizado

        Keywords arguments:

        rent -- variavel do tipo Rent que será validada
        '''
        item=Item(nome=rent.itens)
        item_atual=self.medItens.get_item(item)
        
        if item_atual!=None:
            if item_atual.qnt_emprestar>0:
                return item_atual
            else:
                return "Item indisponível para empréstimo."
        else:
            return "Item inexistente."
    
    def rentup_item(self, rent:Rent):
        ''' Metodo reponsável por criar um novo emprestimo no banco de dados

        Keywords arguments:

        rent -- variavel do tipo Rent que será adicionada ao banco
        '''
        item=self.__validate(rent)
        
        if type(item)==Itens:
            self.repo.insert(rent.to_banco())
            self.repoItens.update_rent(item)
        else:
            return item

    def return_item(self, rent:Rent):
        ''' Metodo reponsável por retornar um emprestimo a coluna de emprestar e adiciona a data de devolução

        Keywords arguments:

        rent -- variavel do tipo Rent que será retornada
        '''
        item=Item(nome=rent.itens)
        item_atual=self.medItens.get_item(item)

        rent2=rent
        rent2.returnDate=datetime.now()

        self.repo.update(rent, rent2)
        self.repoItens.update_return(item_atual)

    def get_history(self):
        '''Retorna o historico de empréstimos'''
        return self.repo.select()

    def get_history_by_item(self, item:Item):
        '''Retorna o historico de empréstimos por item'''
        return self.repo.select_by_item(item)

    def get_history_by_user(self, user:User):
        '''Retorna o historico de empréstimos por usuario'''
        return self.repo.select_by_user(user)
