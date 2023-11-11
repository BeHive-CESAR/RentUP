from fastapi import status
from datetime import datetime
from fastapi.exceptions import HTTPException
from api.entidades.Rent import Rent, ReturnRent
from infra.entities.rent import Rent as RentDB
from api.mediators.user_mediator import UserMediator
from infra.repository.rent_repository import RentRepository
from .item_mediator import ItemMediator, Item, BaseItem, ItensRepository

class RentMediator:
    def __init__(self):
        self.repo=RentRepository()
        self.user_mediator=UserMediator()
        self.item_mediator=ItemMediator()
        self.item_repo=ItensRepository()

    def __validate_rent(self, rent:Rent):
        ''' Metodo reponsável por validar se o Rent pode ser realizado

        Keywords arguments:

        rent -- variavel do tipo Rent que será validada
        '''
        item=BaseItem(nome=rent.itens)
        item_atual=self.item_mediator.get_item(item)
        
        if item_atual is None:
            raise HTTPException(
                detail="Item inexistente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if item_atual.qnt_emprestar==0:
            raise HTTPException(
                detail="Item indisponível para empréstimo",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
    
    def rentup_item(self, rent:Rent):
        ''' Metodo reponsável por criar um novo emprestimo no banco de dados

        Keywords arguments:

        rent -- variavel do tipo Rent que será adicionada ao banco
        '''
        self.__validate_rent(rent)
        item = self.item_mediator.get_item(BaseItem(nome=rent.itens))
        user = self.user_mediator.get_user_by_email(rent.user)

        if user is None:
            raise HTTPException(
                detail="Usuário inexistente",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        rent_db=RentDB(
            user_id=user.id,
            item_id=item.id,
            data_emprestimo=rent.rentDate,
            data_devolucao=None,
            estado=rent.status.name
        )
        
        
        self.repo.insert(rent_db)
        self.item_repo.update_rent(rent.itens)
        

    def return_item(self, rent:ReturnRent):
        ''' Metodo reponsável por retornar um emprestimo a coluna de emprestar e adiciona a data de devolução

        Keywords arguments:

        rent -- variavel do tipo Rent que será retornada
        '''


        item=Item(nome=rent.itens)
        item_atual=self.item_mediator.get_item(item)

        if item_atual is None:
            raise HTTPException(
                detail="Item inexistente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        elif item_atual.qnt_emprestados==0:
            raise HTTPException(
                detail="Item não emprestado",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        rent_update=rent
        rent_update.returnDate=datetime.now()

        self.repo.update(rent, rent_update)
        self.repoItens.update_return(item_atual)

    def get_history(self):
        '''Retorna o historico de empréstimos'''
        return self.repo.select()

    def get_history_by_item(self, item:BaseItem):
        '''Retorna o historico de empréstimos por item'''
        item_on_db=self.item_mediator.get_item(item)

        if item_on_db is None:
            raise HTTPException(
                detail="Item inexistente",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        itens = self.repo.select_by_item(item)
        if itens is None:
            raise HTTPException(
                detail="Nenhum emprestimo encontrado para este item",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return itens

    def get_history_by_user(self, user_email:str):
        '''Retorna o historico de empréstimos por usuario'''
        user = self.user_mediator.get_user(user_email)

        if user is None:
            raise HTTPException(
                detail="Usuário inexistente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        rent_list = self.repo.select_by_user(user)

        if rent_list is None:
            raise HTTPException(
                detail="Nenhum empréstimo encontrado para este usuário",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return rent_list
