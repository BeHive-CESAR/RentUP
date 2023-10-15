from fastapi import APIRouter
from api.entidades.Users import Users

router = APIRouter()

@router.get('/')
async def teste():
    return {"Teste":"testado"}