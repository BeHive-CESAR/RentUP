from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.entidades.Item import Item, BaseItem, ItemDescription, ItemQnt
from api.mediators.item_mediator import ItemMediator
from api.depends import auth_admin
import urllib.parse


class ItemController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/create-item", dependencies=[Depends(auth_admin)]) #o @ pemite alterar a função para adicionar uma propriedade especifica
        async def create_item(item: Item):
            '''
            ### Criar Item

            Cria um novo item no estoque.

            **Endpoint:** `POST /item/create-item`

            **Acesso:** Somente administradores autenticados.

            **Corpo da Requisição:**
            - **nome** (string): Nome do novo item.
            - **qntEstoque** (integer): Quantidade atual em estoque.
            - **qntEmprestar** (integer): Quantidade disponível para empréstimo.
            - **qntEmprestados** (integer): Quantidade atualmente emprestada.
            - **qntDanificados** (integer): Quantidade de itens danificados.
            - **descricao** (string, opcional): Descrição do item.
            - **imagem** (string, opcional): URL da imagem representativa do item.

            **Códigos de Resposta:**
            - **201 Created**: O item foi criado com sucesso.
            - **400 Bad Request**: A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).
            - **401 Unauthorized**: Acesso não autorizado. Somente administradores podem criar itens.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.

            **Exemplo de Uso:**
            ```python
            import requests

            dados_item = {
                "nome": "Novo Item",
                "qntEstoque": 100,
                "qntEmprestar": 80,
                "qntEmprestados": 20,
                "qntDanificados": 2,
                "descricao": "Descrição detalhada do novo item.",
                "imagem": "https://exemplo.com/imagem/novo_item.jpg"
            }

            # Token de autenticação de administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            response = requests.post("https://rentup.up.railway.app/item/create-item", json=dados_item, headers=headers)
            if response.status_code == 201:
                print("Novo item criado com sucesso.")
            else:
                print("Falha na criação do item. Verifique os dados fornecidos ou suas permissões de administrador.")

            '''
            ItemMediator().create_item(item)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Item criado com sucesso"}
            )

        @self.router.get("/get-items")
        async def get_items():
            '''
            ### Obter Todos os Itens

            Recupera uma lista de todos os itens disponíveis no estoque.

            **Endpoint:** `GET /item/get-items`

            **Acesso:** Somente usuários autenticados.

            **Parâmetros da Requisição:**
            - Nenhum.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna uma lista de todos os itens.
            - **404 Not Found**: Não foram encontrados itens no estoque.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação de usuário
            headers = {"Authorization": "Bearer <token_do_usuario>"}

            response = requests.get("https://rentup.up.railway.app/item/get-items", headers=headers)
            if response.status_code == 200:
                itens = response.json()
                for item in itens:
                    print(item)
            else:
                print("Nenhum item encontrado no estoque.")
            '''
            itens_list = ItemMediator().get_all_items()
            item_data = [{
                'nome_item': item.nome_item,
                'qnt_total': item.qnt_total,
                'qnt_estoque': item.qnt_estoque,
                'qnt_emprestar': item.qnt_emprestar,
                'qnt_emprestados': item.qnt_emprestados,
                'qnt_danificados': item.qnt_danificados,
                'descricao': item.descricao,
                'imagem': item.imagem } for item in itens_list]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"itens": item_data}
            )
        
        @self.router.get("/get-item-by-name")
        async def get_item(item: str):
            '''
            ### Obter Item por Nome

            Recupera informações de um item específico com base no seu nome.

            **Endpoint:** `GET /item/get-item-by-name?item=<nome_do_item>`

            **Parâmetros da Requisição:**
            - **nome** (string): O nome do item que deseja consultar.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna informações do item com o nome correspondente.
            - **404 Not Found**: Nenhum item com o nome especificado foi encontrado no estoque.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.

            **Exemplo de Uso:**
            ```python
            import requests

            nome_do_item = "NomeDoItem"

            # Token de autenticação de usuário
            headers = {"Authorization": "Bearer <token_do_usuario>"}

            response = requests.get(f"https://rentup.up.railway.app/item/get-item-by-name?nome={nome_do_item}", headers=headers)
            if response.status_code == 200:
                item = response.json()
                print(f"Informações do item {nome_do_item}: {item}")
            else:
                print(f"Item com o nome {nome_do_item} não encontrado no estoque.")
            '''
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
                'descricao': item.descricao,
                'imagem': item.imagem }
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"item": item_data}
            )

        @self.router.put("/edit-qnt-item", dependencies=[Depends(auth_admin)])
        async def edit_qnt_item(item: ItemQnt):
            '''
            ### Editar Quantidades do Item

            Edita as quantidades de um item existente no estoque.

            **Endpoint:** `PUT /item/edit-qnt-item`

            **Acesso:** Somente administradores autenticados.

            **Corpo da Requisição:**
            - **nome** (string): Nome do item a ser editado.
            - **qntEstoque** (integer): Nova quantidade atual em estoque.
            - **qntEmprestar** (integer): Nova quantidade disponível para empréstimo.
            - **qntEmprestados** (integer): Nova quantidade atualmente emprestada.
            - **qntDanificados** (integer): Nova quantidade de itens danificados.

            **Códigos de Resposta:**
            - **200 OK**: A edição do item foi bem-sucedida. As informações do item foram atualizadas com sucesso.
            - **400 Bad Request**: A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).
            - **401 Unauthorized**: Acesso não autorizado. Somente administradores podem editar itens.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.
            - **404 Not Found**: Nenhum item com o nome original especificado foi encontrado no estoque.

            **Exemplo de Uso:**
            ```python
            import requests

            dados_edicao_item = {
                "nome": "NomeDoItem",
                "qntEstoque": 120,
                "qntEmprestar": 90,
                "qntEmprestados": 30,
                "qntDanificados": 5,
            }

            # Token de autenticação de administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            response = requests.put("https://rentup.up.railway.app/item/edit-qnt-item", json=dados_edicao_item, headers=headers)
            if response.status_code == 200:
                print(f"Informações do item {dados_edicao_item['nome_original']} foram atualizadas com sucesso.")
            else:
                print(f"Nenhum item com o nome original {dados_edicao_item['nome_original']} encontrado para edição.")
            '''
            ItemMediator().edit_qnt_item(item)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Item editado com sucesso"}
            )
        
        @self.router.put("/edit-infos-item", dependencies=[Depends(auth_admin)])
        async def edit_infos_item(item_atual:BaseItem, novo_item: ItemDescription):
            '''
            ### Editar informações do Item

            Edita as informações de um item existente no estoque.

            **Endpoint:** `PUT /item/edit-item`

            **Acesso:** Somente administradores autenticados.

            **Corpo da Requisição:**
            - **nome_atual** (string): O nome original do item a ser editado.
            - **nome** (string): Novo nome do item.
            - **descricao** (string, opcional): Nova descrição do item.
            - **imagem** (string, opcional): Nova URL da imagem representativa do item.

            **Códigos de Resposta:**
            - **200 OK**: A edição do item foi bem-sucedida. As informações do item foram atualizadas com sucesso.
            - **400 Bad Request**: A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).
            - **401 Unauthorized**: Acesso não autorizado. Somente administradores podem editar itens.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.
            - **404 Not Found**: Nenhum item com o nome original especificado foi encontrado no estoque.
            - **409 Conflict**: Já existe um item com o nome especificado.

            **Exemplo de Uso:**
            ```python
            import requests


            dados_edicao_item = {
                "item_atual": {
                    "nome": "NomeOriginalDoItem"
                },
                "novo_item": {
                    "nome": "Novo Nome do Item",
                    "descricao": "Nova descrição detalhada do item.",
                    "imagem": "https://exemplo.com/imagem/novo_item.jpg",
                    "categoria": "Nova categoria do item."
                }
            }

            # Token de autenticação de administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            response = requests.put("https://rentup.up.railway.app/item/edit-infos-item", json=dados_edicao_item, headers=headers)
            if response.status_code == 200:
                print(f"Informações do item {dados_edicao_item['item_atual']['nome']} foram atualizadas com sucesso.")
            else:
                print(f"Nenhum item com o nome original {dados_edicao_item['item_atual']['nome']} encontrado para edição.")
            '''
            ItemMediator().edit_infos_item(item_atual, novo_item)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Item editado com sucesso"}
            )

        
        @self.router.delete("/delete-item", dependencies=[Depends(auth_admin)])
        async def delete_item(item: BaseItem):
            '''
            ### Excluir Item

            Exclui um item do estoque.

            **Endpoint:** `DELETE /item/delete-item`

            **Acesso:** Somente administradores autenticados.

            **Corpo da Requisição:**
            - **nome** (string): O nome do item a ser excluído.

            **Códigos de Resposta:**
            - **200 OK **: A exclusão do item foi bem-sucedida. O item foi removido do estoque.
            - **400 Bad Request**: A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).
            - **401 Unauthorized**: Acesso não autorizado. Somente administradores podem criar itens.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.
            - **404 Not Found**: Nenhum item com o nome especificado foi encontrado no estoque.

            **Exemplo de Uso:**
            ```python
            import requests

            dados_exclusao_item = {
                "nome": "NomeDoItemAExcluir"
            }

            # Token de autenticação de administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            response = requests.delete("https://rentup.up.railway.app/item/delete-item", json=dados_exclusao_item, headers=headers)
            if response.status_code == 204:
                print(f"Item {dados_exclusao_item['nome']} excluído com sucesso.")
            else:
                print(f"Nenhum item com o nome {dados_exclusao_item['nome']} encontrado para exclusão.")

            '''
            ItemMediator().delete_item(item)
            return JSONResponse(
                content={"message": "Item excluído com sucesso"},
                status_code=status.HTTP_200_OK,
            )            