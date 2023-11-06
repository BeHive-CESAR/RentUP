from fastapi import FastAPI
from api.rotas import router
from infra.configs.connection import DBConnectionHandler

app = FastAPI()

with DBConnectionHandler() as db:
    db.create_all_tables()

@app.get('/')
async def root():
    return {"Bem vindo ao RentUP": "conectado"}

app.include_router(router, prefix='')