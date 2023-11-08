from fastapi import FastAPI
from api.rotas import router
from infra.configs.connection import DBConnectionHandler

description = '''
# **RentUP APIa**

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

'''

tags_metadata = [
    {
        "name": "Users",
        "description": "Operações com usuarios. A lógica de **login** está aqui"
        
    },
    {
        "name": "Itens",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "description": "Gerenciamento de Itens no estoque.",
    },
    {
        "name": "Root",
        "description": "Endpoints"
    }
]

app = FastAPI(title='RentUP API',
              description=description,
              version='0.0.1',
              summary="Garagino's favorite API",
              contact={
                    "name": 'Garagino',
                    "url": 'https://github.com/garagino'
              },
              openapi_tags=tags_metadata
              )

with DBConnectionHandler() as db:
    db.create_all_tables()

@app.get('/', tags=['Root'])
async def root():
    return {"Bem vindo ao RentUP": "conectado"}

app.include_router(router, prefix='')