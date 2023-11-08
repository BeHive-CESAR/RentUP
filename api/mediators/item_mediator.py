from fastapi import status
from fastapi.exceptions import HTTPException
from api.entidades.Item import Item, BaseItem
from infra.repository.itens_repository import ItensRepository, Itens

class ItemMediator:
    def __init__(self):
        self.repo = ItensRepository()    

    def __validate_item(self, item:Item):
        '''Meotodo privado responsavel por validar o Item, caso esteja tudo OK, retorna False

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
        self.__validate_item(item)
        
        if self.get_item(item):
            raise HTTPException(
                detail="Item já existente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        self.repo.insert(item.to_banco())
        
    
    def edit_item(self, item1:BaseItem, item2:Item):
        '''Realiza a validação do item e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa o item e edita-o. Caso não retorna uma mensagem de erro

        Keyword arguments:

        item1 -- Objeto do tipo BaseItem que será buscado e editado
        
        item2 -- Objeto do tipo Item que deverá possuir os novos dados para substituir o item1 no banco
        '''
        self.__validate_item(item2)
        
        if self.get_item(item1) is None:
            raise HTTPException(
                detail="Item não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        original_item = Itens(nome_item=item1.nome.capitalize()) 
        self.repo.update(original_item, item2.to_banco())
        
    
    def delete_item(self, item:BaseItem):
        '''Metodo responsavel por deletar um Item do banco de dados

        Keyword arguments:

        item -- Objeto do tipo Item que buscado e deletado
        '''
        item_to_delete = self.get_item(item)
        
        self.repo.delete(item_to_delete)
    
    def get_items(self):
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

        item -- Objeto do tipo Item que será buscado
        '''
        item = Itens(nome_item=item.nome.capitalize())
        item_on_db = self.repo.select_by_item(item)
        if item_on_db is None:
            raise HTTPException(
                detail="Item não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return item_on_db
    
    