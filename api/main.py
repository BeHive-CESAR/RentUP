from fastapi import FastAPI
from api.rotas import router

app = FastAPI()

@app.get('/')
async def root():
    return {"Bem vindo ao RentUP": "conectado"}

app.include_router(router, prefix='')