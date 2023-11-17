from fastapi import status
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from api.entidades.Item import Item, BaseItem
from infra.repository.itens_repository import ItensRepository, Itens
from sqlalchemy.exc import ProgrammingError

class ItemMediator:
    def __init__(self):
        self.repo = ItensRepository()    

    def __validate_item(self, item:Item):
        '''DEPRECATED:
        Meotodo privado responsavel por validar o Item, caso esteja tudo OK, retorna False

        Keyword arguments:

        item -- Objeto do tipo Item que será validado
        '''
        if item.qntTotal < 0 or item.qntEstoque < 0 or item.qntEmprestar < 0 or item.qntEmprestados < 0 or item.qntDanificados < 0:
            raise HTTPException(
                detail="Quantidade negativa de itens",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        elif item.qntTotal != item.qntEstoque+item.qntEmprestar+item.qntEmprestados+item.qntDanificados:
            raise HTTPException(
                detail="Quantidade de itens total invalida",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
    
    def create_item(self, item:Item):
        '''Realiza a validação do item e verifica se o mesmo não existe no banco. Caso esteja tudo OK cria o item no banco de dados. Caso não retorna uma mensagem de erro
        
        Keyword arguments:

        item -- Objeto do tipo Item que será criado no banco de dados
        '''
        # self.__validate_item(item)
        
        if self.get_item(item):
            raise HTTPException(
                detail="Item já existente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        item_db = Itens(
            nome_item=item.nome.capitalize(),
            qnt_estoque=item.qntEstoque,
            qnt_emprestar=item.qntEmprestar,
            qnt_emprestados=item.qntEmprestados,
            qnt_danificados=item.qntDanificados,
            descricao=item.descricao,
            qnt_total=sum([item.qntEstoque, item.qntEmprestar, item.qntEmprestados, item.qntDanificados])
        )
        self.repo.insert(item_db)
        
    
    def edit_item(self, item1:BaseItem, item2:Item):
        '''Realiza a validação do item e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa o item e edita-o. Caso não retorna uma mensagem de erro

        Keyword arguments:

        item1 -- Objeto do tipo BaseItem que será buscado e editado
        
        item2 -- Objeto do tipo Item que deverá possuir os novos dados para substituir o item1 no banco
        '''
        # self.__validate_item(item2)
        
        if self.get_item(item1) is None:
            raise HTTPException(
                detail="Item não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        original_item = Itens(nome_item=item1.nome.capitalize()) 
        new_item = Itens(
            nome_item=item2.nome.capitalize(),
            qnt_estoque=item2.qntEstoque,
            qnt_emprestar=item2.qntEmprestar,
            qnt_emprestados=item2.qntEmprestados,
            qnt_danificados=item2.qntDanificados,
            descricao=item2.descricao,
            qnt_total=sum([item2.qntEstoque, item2.qntEmprestar, item2.qntEmprestados, item2.qntDanificados])
        )
        self.repo.update(original_item, new_item)
        
    
    def delete_item(self, item:BaseItem):
        '''Metodo responsavel por deletar um Item do banco de dados

        Keyword arguments:

        item -- Objeto do tipo BaseItem que buscado e deletado
        '''
        item_to_delete = self.get_item(item)

        if item_to_delete is None:
            raise HTTPException(
                detail="Item não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        try:
            self.repo.delete(item_to_delete)
        except ProgrammingError:
            raise HTTPException(
                detail="Item não pode ser deletado pois está sendo usado em um emprestimo",
                status_code=status.HTTP_409_CONFLICT
            )
    
    def get_all_items(self):
        '''Metodo responsavel por buscar todos os Itens no banco de dados'''
        itens = self.repo.select()
        if itens is None:
            raise HTTPException(
                detail="Nenhum item encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return itens
    
    def get_item(self, item:BaseItem):
        '''Metodo responsavel por buscar o Item correspondente no banco de dados, caso não encontrado retorna None

        Keyword arguments:

        item -- Objeto do tipo BaseItem que será buscado
        '''
        item = Itens(nome_item=item.nome.capitalize())
        item_on_db = self.repo.select_by_item(item)
        
        return item_on_db
    
    def get_item_by_id(self, id:int):
        '''Metodo responsavel por buscar o Item correspondente no banco de dados, caso não encontrado retorna None

        Keyword arguments:

        id -- Objeto do tipo int que será buscado
        '''
        item_on_db = self.repo.select_item_by_id(id)
        
        return item_on_db
    
    