from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.mediators.item_mediator import ItemMediator
from api.mediators.rent_mediator import RentMediator

class DataController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get('/dashboard')
        async def data():
            '''
            ### Painel de Controle - Dados Gerais

            Recupera dados gerais do sistema para um painel de controle.

            **Endpoint:** `GET /data/dashboard`

            **Acesso:** Somente administradores autenticados.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna dados gerais do sistema.
            - **401 Unauthorized**: Acesso não autorizado. O usuário não possui privilégios de administrador.

            **Formato dos Dados de Resposta:**
            ```json
            {
            "total_itens": 120,
            "total_danificados": 10,
            "total_emprestimos_andamento": 5,
            "itens_mais_danificados": [
                {
                "nome": "Arduino",
                "danificados": 5
                },
                {
                "nome": "Raspberry Pi",
                "danificados": 3
                },
                {
                "nome": "ProtoBoard",
                "danificados": 2
                }
            ],
            "itens_mais_emprestados": [
                {
                "nome": "Arduino",
                "qnt_emprestados": 3
                },
                {
                "nome": "Raspberry Pi",
                "qnt_emprestados": 2
                },
                {
                "nome": "ProtoBoard",
                "qnt_emprestados": 1
                }
            ]
            }
            ```

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação do administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            response = requests.get("https://rentup.com/data/dashboard", headers=headers)
            if response.status_code == 200:
                dados_painel_controle = response.json()
                print(dados_painel_controle)
            else:
                print("Falha ao recuperar dados do painel de controle. Verifique suas permissões de administrador.")
            '''
            try:
                list_itens = [{
                    "nome":item.nome_item,
                    'danificados':item.qnt_danificados,
                    'qnt_total': item.qnt_total,
                    'qnt_emprestados': item.qnt_emprestados
                } for item in ItemMediator().get_all_items()]

                list_emprestimos = [{
                    "status":emprestimo.estado
                } for emprestimo in RentMediator().get_history()]

                total_itens = sum([item['qnt_total'] for item in list_itens])
                total_danificados = sum([item['danificados'] for item in list_itens])
                total_emprestimos_andamento = sum([1 for emprestimo in list_emprestimos if emprestimo['status'] == 'APROVED'])

                itens_mais_danificados = sorted(list_itens, key=lambda x: x['danificados'], reverse=True)[:3]
                itens_mais_emprestados = sorted(list_itens, key=lambda x: x['qnt_emprestados'], reverse=True)[:3]

                itens_mais_danificados = [{'nome': item['nome'], 'danificados': item['danificados']} for item in itens_mais_danificados]
                itens_mais_emprestados = [{'nome': item['nome'], 'qnt_emprestados': item['qnt_emprestados']} for item in itens_mais_emprestados]



            except Exception as e:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(e)})
            else:
                return JSONResponse(status_code=status.HTTP_200_OK, content={
                    "total_itens": total_itens,
                    "total_danificados": total_danificados,
                    "total_emprestimos_andamento": total_emprestimos_andamento,
                    "itens_mais_danificados": itens_mais_danificados,
                    "itens_mais_emprestados": itens_mais_emprestados
                })

            
