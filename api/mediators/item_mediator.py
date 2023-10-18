from entidades.Item import Item
from infra.repository.itens_repository import ItensRepository

class ItemMediator:      

    def __validate_item(self, item:Item):
        if item.qntTotal < 0 or item.qntEstoque < 0 or item.qntEmprestar < 0 or item.qntEmprestados < 0 or item.qntDanificados < 0:
            return "Quantidade negativa de itens"
        elif item.qntTotal != item.qntEstoque+item.qntEmprestar+item.qntEmprestados+item.qntDanificados:
            return "Quantidade de itens total invalida"
        
        return True
    
    def create_item(self, item:Item):
        validacao = self.__validate_item(item)
        if validacao:
            ItensRepository.insert(item)
        else:
            return validacao
    
    def edit_item(self, item1:Item, item2:Item):
        validacao = self.__validate_item(item2)
        if validacao:
            ItensRepository.update(item1, item2)
            return validacao
        else:
            return validacao
    
    def get_items():
        return ItensRepository.select()
    
    def get_item(item:Item):
        return ItensRepository.select_by_item(item)