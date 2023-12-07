from fastapi import status
from fastapi.exceptions import HTTPException
from api.entidades.Item import ItemQnt, BaseItem, ItemDescription, Item
from infra.repository.itens_repository import ItensRepository, Itens
from api.mediators.category_mediator import CategoryMediator
from sqlalchemy.exc import ProgrammingError

class ItemMediator:
    def __init__(self):
        self.repo = ItensRepository()    
        self.category_mediator = CategoryMediator()

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
        
        categoria = self.category_mediator.get_category(item.categoria)

        if categoria is None:
            raise HTTPException(
                detail="Categoria não existente",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        item_db = Itens(
            nome_item=item.nome.capitalize(),
            qnt_estoque=item.qntEstoque,
            qnt_emprestar=item.qntEmprestar,
            qnt_emprestados=item.qntEmprestados,
            qnt_danificados=item.qntDanificados,
            descricao=item.descricao,
            categoria_id=categoria.id,
            qnt_total=sum([item.qntEstoque, item.qntEmprestar, item.qntEmprestados, item.qntDanificados])
        )
        self.repo.insert(item_db)
        
    
    def edit_qnt_item(self, item:ItemQnt):
        '''Realiza a validação do item e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa
        o item e edita as quantidades no banco de dados. Caso não retorna uma mensagem de erro

        Keyword arguments:

        item -- Objeto do tipo Item que será buscado e editado
        '''
        # self.__validate_item(item2)
        
        if self.get_item(item) is None:
            raise HTTPException(
                detail="Item não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        new_item = Itens(
            id = self.get_item(item).id,
            qnt_estoque=item.qntEstoque,
            qnt_emprestar=item.qntEmprestar,
            qnt_emprestados=item.qntEmprestados,
            qnt_danificados=item.qntDanificados,
            qnt_total=sum([item.qntEstoque, item.qntEmprestar, item.qntEmprestados, item.qntDanificados])
        )
        self.repo.update_qnt(new_item)
    
    def edit_infos_item(self, item_atual:BaseItem, novo_item:ItemDescription):
        '''Realiza a validação do item e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa
        o item e edita as informações no banco de dados. Caso não retorna uma mensagem de erro

        Keyword arguments:

        item_atual -- Objeto do tipo BaseItem que será buscado para ser alterado
        novo_item -- Objeto do tipo ItemDescription que será inserido no lugar do item_atual
        '''
        
        if self.get_item(item_atual) is None:
            raise HTTPException(
                detail="Item não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if novo_item.nome.capitalize() != item_atual.nome.capitalize():
            if self.get_item(novo_item):
                raise HTTPException(
                    detail="Item com esse nome já existe",
                    status_code=status.HTTP_409_CONFLICT
                )
        
        categoria = self.category_mediator.get_category(novo_item.categoria)

        if categoria is None:
            raise HTTPException(
                detail="Categoria não existente",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        new_item = Itens(
            id = self.get_item(item_atual).id,
            nome_item=novo_item.nome.capitalize(),
            descricao=novo_item.descricao,
            imagem=novo_item.imagem,
            categoria_id=categoria.id
        )
        self.repo.update_infos(new_item)
        
    
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
    
    def get_items_by_category(self, categoria:str):
        '''Metodo responsavel por buscar os Itens correspondentes no banco de dados, caso não encontrado retorna None

        Keyword arguments:

        categoria -- Objeto do tipo str que será buscado
        '''
        categoria = self.category_mediator.get_category(categoria)

        itens_on_db = self.get_all_items()
        itens_on_db = [item for item in itens_on_db if item.categoria_id == categoria.id]
        
        if len(itens_on_db) == 0:
            raise HTTPException(
                detail="Nenhum item encontrado para essa categoria",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return itens_on_db
    
    