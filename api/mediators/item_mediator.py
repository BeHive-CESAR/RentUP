from api.entidades.Item import Item
from infra.repository.itens_repository import ItensRepository

class ItemMediator:
    def __init__(self) -> None:
        self.repo = ItensRepository()    

    def __validate_item(self, item:Item):
        '''
        Valida as quantidades de itens, caso esteja tudo OK, retorna False
        '''
        if item.qntTotal < 0 or item.qntEstoque < 0 or item.qntEmprestar < 0 or item.qntEmprestados < 0 or item.qntDanificados < 0:
            return "Quantidade negativa de itens"
        elif item.qntTotal != item.qntEstoque+item.qntEmprestar+item.qntEmprestados+item.qntDanificados:
            return "Quantidade de itens total invalida"
        
        return False
    
    def create_item(self, item:Item):
        validacao = self.__validate_item(item)
        if not validacao:
            if self.get_item(item) == None:
                self.repo.insert(item.to_banco())
            else:
                return "Item já existente"
        else:
            return validacao
    
    def edit_item(self, item1:Item, item2:Item):
        validacao = self.__validate_item(item2)
        if not validacao:
            if self.get_item(item1) != None:
                self.repo.update(item1.to_banco(), item2.to_banco())
            else:
                return f"Item {item1.nome} não existe"
        else:
            return validacao
    
    def delete_item(self, item:Item):
        self.repo.delete(item.to_banco())
    
    def get_items(self):
        return self.repo.select()
    
    def get_item(self, item:Item):
        return self.repo.select_by_item(item.to_banco())