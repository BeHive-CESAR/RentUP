from fastapi import FastAPI
from api.rotas import router

app = FastAPI()

app.include_router(router, prefix='')