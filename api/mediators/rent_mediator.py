from fastapi import status
from fastapi.exceptions import HTTPException
from api.entidades.Rent import Rent
from infra.entities.rent import Rent as RentDB
from api.mediators.user_mediator import UserMediator
from infra.repository.rent_repository import RentRepository
from .item_mediator import ItemMediator, BaseItem, ItensRepository, Itens
from api.entidades.Status import Status
from datetime import datetime

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
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if item_atual.qnt_emprestar==0:
            raise HTTPException(
                detail="Item indisponível para empréstimo",
                status_code=status.HTTP_409_CONFLICT
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
                status_code=status.HTTP_404_NOT_FOUND
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
        

    def return_item(self, rent_id:int):
        ''' Metodo reponsável por atualizar o emprestimo no banco de dados para devolvido e atualizar a quantidade de itens disponíveis'''

        rent_on_db=self.repo.select_rent_by_id(rent_id)
        if rent_on_db is None:
            raise HTTPException(
                detail="Emprestimo não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if rent_on_db.estado == Status.RETURNED.name:
            raise HTTPException(
                detail="Item já devolvido",
                status_code=status.HTTP_409_CONFLICT
            )
        
        self.repo.update_status(rent_on_db, Status.RETURNED.name)
        self.repo.update_return_date(rent_on_db.id, datetime.now())
        self.item_repo.update_return(rent_on_db.item_id)

    def get_history(self):
        '''Retorna o historico de empréstimos'''
        rent = self.repo.select()
        if rent is None:
            raise HTTPException(
                detail="Nenhum emprestimo encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return rent

    def get_history_by_item(self, item:BaseItem):
        '''Retorna o historico de empréstimos por item'''
        item_on_db=self.item_mediator.get_item(item)

        if item_on_db is None:
            raise HTTPException(
                detail="Item inexistente",
                status_code=status.HTTP_404_NOT_FOUND
            )

        itens = self.repo.select_by_item(Itens(nome_item=item.nome.capitalize()))
        if itens is None:
            raise HTTPException(
                detail="Nenhum emprestimo encontrado para este item",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return itens

    def get_history_by_user(self, user_email:str):
        '''Retorna o historico de empréstimos por usuario'''
        user = self.user_mediator.get_user_by_email(user_email)

        if user is None:
            raise HTTPException(
                detail="Usuário inexistente",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        rent_list = self.repo.select_by_user(user.email)

        if rent_list is None:
            raise HTTPException(
                detail="Nenhum empréstimo encontrado para este usuário",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return rent_list
    
    def update_status(self, id:int, stat:Status):
        '''Atualiza o status do emprestimo'''

        rent_on_db = self.repo.select_rent_by_id(id)

        if rent_on_db is None:
            raise HTTPException(
                detail="Emprestimo não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )

        self.repo.update_status(rent_on_db, stat)
