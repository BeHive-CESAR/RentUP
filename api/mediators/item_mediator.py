from api.entidades.Item import Item
from infra.repository.itens_repository import ItensRepository

class ItemMediator:
    def __init__(self):
        self.repo = ItensRepository()    

    def __validate_item(self, item:Item):
        '''Meotodo privado responsavel por validar o Item, caso esteja tudo OK, retorna False

        Keyword arguments:

        item -- Objeto do tipo Item que será validado
        '''
        if item.qntTotal < 0 or item.qntEstoque < 0 or item.qntEmprestar < 0 or item.qntEmprestados < 0 or item.qntDanificados < 0:
            return "Quantidade negativa de itens"
        elif item.qntTotal != item.qntEstoque+item.qntEmprestar+item.qntEmprestados+item.qntDanificados:
            return "Quantidade de itens total invalida"
        
        return False
    
    def create_item(self, item:Item):
        '''Realiza a validação do item e verifica se o mesmo não existe no banco. Caso esteja tudo OK cria o item no banco de dados. Caso não retorna uma mensagem de erro
        
        Keyword arguments:

        item -- Objeto do tipo Item que será criado no banco de dados
        '''
        validacao = self.__validate_item(item)
        if not validacao:
            if self.get_item(item) == None:
                self.repo.insert(item.to_banco())
            else:
                return "Item já existente"
        else:
            return validacao
    
    def edit_item(self, item1:Item, item2:Item):
        '''Realiza a validação do item e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa o item e edita-o. Caso não retorna uma mensagem de erro

        Keyword arguments:

        item1 -- Objeto do tipo Item que será buscado e editado
        
        item2 -- Objeto do tipo Item que deverá possuir os novos dados para substituir o item1 no banco
        '''
        validacao = self.__validate_item(item2)
        if not validacao:
            if self.get_item(item1) != None:
                self.repo.update(item1.to_banco(), item2.to_banco())
            else:
                return f"Item {item1.nome} não existe"
        else:
            return validacao
    
    def delete_item(self, item:Item):
        '''Metodo responsavel por deletar um Item do banco de dados

        Keyword arguments:

        item -- Objeto do tipo Item que buscado e deletado
        '''
        self.repo.delete(item.to_banco())
    
    def get_items(self):
        '''Metodo responsavel por buscar todos os Itens no banco de dados'''
        return self.repo.select()
    
    def get_item(self, item:Item):
        '''Metodo responsavel por buscar o Item correspondente no banco de dados, caso não encontrado retorna None

        Keyword arguments:

        item -- Objeto do tipo Item que será buscado
        '''
        return self.repo.select_by_item(item.to_banco())
    
    