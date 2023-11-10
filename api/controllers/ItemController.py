from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.entidades.Item import Item, BaseItem
from api.mediators.item_mediator import ItemMediator
from api.depends import auth_admin, auth_wrapper
import urllib.parse


class ItemController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/create-item", dependencies=[Depends(auth_admin)])
        async def create_item(item: Item):
            ItemMediator().create_item(item)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Item criado com sucesso"}
            )

        @self.router.get("/get-items")
        async def get_items():
            itens_list = ItemMediator().get_all_items()
            item_data = [{
                'nome_item': item.nome_item,
                'qnt_total': item.qnt_total,
                'qnt_estoque': item.qnt_estoque,
                'qnt_emprestar': item.qnt_emprestar,
                'qnt_emprestados': item.qnt_emprestados,
                'qnt_danificados': item.qnt_danificados,
                'descricao': item.descricao } for item in itens_list]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"itens": item_data}
            )
        
        @self.router.get("/get-item-by-name")
        async def get_item(item: str):
            item = urllib.parse.unquote(item)
            item = ItemMediator().get_item(BaseItem(nome=item))
            if item is None:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"message": "Item não encontrado"}
                )
            item_data = {
                'nome_item': item.nome_item,
                'qnt_total': item.qnt_total,
                'qnt_estoque': item.qnt_estoque,
                'qnt_emprestar': item.qnt_emprestar,
                'qnt_emprestados': item.qnt_emprestados,
                'qnt_danificados': item.qnt_danificados,
                'descricao': item.descricao }
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"item": item_data}
            )

        @self.router.put("/edit-item", dependencies=[Depends(auth_admin)])
        async def edit_item(item1: BaseItem, item2: Item):
            ItemMediator().edit_item(item1, item2)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Item editado com sucesso"}
            )
        
        @self.router.delete("/delete-item", dependencies=[Depends(auth_admin)])
        async def delete_item(item: BaseItem):
            ItemMediator().delete_item(item)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Item deletado com sucesso"}
            )            