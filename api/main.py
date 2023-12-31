from fastapi import FastAPI
from api.rotas import router
from infra.configs.connection import DBConnectionHandler

description = '''
A **RentUP API** foi desenvolvida para resolver os desafios de gerenciamento de estoque e empréstimos em laboratórios maker.

## Itens

Você pode realizar as seguintes operações com itens:

- **Adicionar**: Crie novos itens no estoque.
- **Editar**: Atualize informações de itens existentes.
- **Visualizar todos**: Obtenha uma lista de todos os itens disponíveis no estoque.

## Usuários

Para gerenciar usuários, a API oferece as seguintes funcionalidades:

- **Registro**: Cadastre-se como um novo usuário.
- **Login**: Faça login na sua conta de usuário.
- **Listar todos os usuários**: Obtenha uma lista de todos os usuários registrados na plataforma.

## Empréstimos

Em relação a empréstimos, a **RentUP API** oferece as seguintes funcionalidades:

- **Solicitar itens emprestados**: Usuários podem solicitar a locação de itens do estoque.
- **Devolver itens emprestados**: Usuários podem registrar a devolução dos itens emprestados.
- **Autorização de empréstimos (apenas para administradores)**: Administradores têm a capacidade de autorizar ou negar pedidos de empréstimos.
- **Acompanhamento da situação dos empréstimos**: Todos os usuários podem acompanhar o status de seus pedidos de empréstimos.

A **RentUP API** é uma ferramenta poderosa para facilitar o controle de recursos, gestão de usuários e todo o ciclo de empréstimos de itens em laboratórios maker.

## Dados

O **módulo de Dados** da API oferece endpoints para a obtenção de informações essenciais que podem ser utilizadas na criação de gráficos, facilitando a tomada de decisão
por parte dos administradores. Esses dados oferecem insights valiosos sobre o estado e o desempenho do sistema, contribuindo para uma gestão eficiente e informada.

'''

tags_metadata = [
    {
        "name": "Users",
        "description": "Operações com usuarios."
        
    },
    {
        "name": "Itens",
        "description": "Gerenciamento de Itens no estoque.",
    },
    {
        "name": "Rent",
        "description": "Operações com empréstimos"
    },
    {
        "name": "Data",
        "description": "Dados para o dashboard"
    
    }
]

app = FastAPI(title='RentUP API',
              description=description,
              version='0.0.2',
              summary="Garagino's favorite API",
              contact={
                    "name": 'Garagino',
                    "url": 'https://github.com/garagino'
              },
              openapi_tags=tags_metadata,
              openapi_url='/rentup.json',
              redoc_url=False
              )

with DBConnectionHandler() as db:
    db.create_all_tables()

@app.get('/', tags=['Root'], include_in_schema=False)
async def root():
    return {"Bem vindo ao RentUP": "conectado"}

app.include_router(router, prefix='')