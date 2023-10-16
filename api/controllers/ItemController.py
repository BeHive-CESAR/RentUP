from fastapi import APIRouter
from api.entidades.Item import Item

class ItemController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/")
        async def teste(item: Item):
            return item

        @self.router.get("/get")
        async def read_item(item_id: int):
            return {"item_id": item_id}