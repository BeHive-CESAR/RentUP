from fastapi import APIRouter
from api.entidades.Item import Item

router = APIRouter()

@router.get("/")
async def teste():
    return {"Teste":"Testado"}