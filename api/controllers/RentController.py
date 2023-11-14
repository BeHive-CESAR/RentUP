from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from api.mediators.rent_mediator import RentMediator, Rent, Status, UserMediator, ItemMediator
from api.mediators.item_mediator import BaseItem
from api.depends import auth_admin


class RentController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/rent")
        def rent_item(rent: Rent):
            '''
            ### Realizar Empréstimo

            Realiza um novo empréstimo de item no sistema.

            **Endpoint:** `POST /rent/rent`

            **Acesso:** Somente usuários autenticados.

            **Parâmetros da Requisição:**
            - **Rent** (objeto): Objeto contendo as informações do empréstimo.
                - **user** (string): E-mail do usuário solicitante do empréstimo.
                - **itens** (string): Nome do item a ser emprestado.
                - **rentDate** (string): Data e hora do empréstimo no formato ISO 8601 (por exemplo, "2023-11-13T09:35:46.389Z").
                - **status** (string, opcional): Status do empréstimo (padrão é "WAITING").

            **Códigos de Resposta:**
            - **201 Created**: O empréstimo foi realizado com sucesso.
            - **400 Bad Request**: A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).
            - **403 Forbidden**: Acesso não autorizado. O usuário não está autenticado.
            - **404 Not Found**: Não foram encontrados itens ou usuário no sistema.
            - **409 Conflict**: Conflito na solicitação de empréstimo (por exemplo, item já emprestado).

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação do usuário
            headers = {"Authorization": "Bearer <token_do_usuario>"}

            # Dados do empréstimo
            dados_emprestimo = {
                "user": "usuario@example.com",
                "itens": "Item A",
                "rentDate": "2023-11-13T09:35:46.389Z",
                "status": "WAITING"
            }

            response = requests.post("https://rentup.com/rent/rent", json=dados_emprestimo, headers=headers)
            if response.status_code == 201:
                print("Empréstimo realizado com sucesso.")
            else:
                print("Falha ao realizar o empréstimo. Verifique os dados fornecidos ou suas permissões de usuário.")

            '''
            RentMediator().rentup_item(rent)
            return JSONResponse(
                content='Empréstimo realizado com sucesso',
                status_code=status.HTTP_201_CREATED
            )

        @self.router.put("/return")
        def return_item(rent_id:int):
            '''
            ### Realizar Devolução

            Realiza a devolução de um item emprestado no sistema.

            **Endpoint:** `PUT /rent/return?rent_id=<rent_id>`

            **Acesso:** Somente usuários autenticados.

            **Parâmetros da Requisição:**
            - **rent_id** (string): ID único do empréstimo que será devolvido.

            **Códigos de Resposta:**
            - **200 OK**: A devolução do item foi realizada com sucesso.
            - **403 Forbidden**: Acesso não autorizado. O usuário não está autenticado.
            - **404 Not Found**: Nenhum empréstimo com o ID especificado foi encontrado no sistema.
            - **409 Conflict**: Conflito na devolução (por exemplo, item já devolvido anteriormente).

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação do usuário
            headers = {"Authorization": "Bearer <token_do_usuario>"}

            # ID do empréstimo a ser devolvido
            rent_id = "123"

            response = requests.put(f"https://rentup.com/rent/return?rent_id={rent_id}", headers=headers)
            if response.status_code == 200:
                print(f"Devolução do item para o empréstimo {rent_id} realizada com sucesso.")
            else:
                print(f"Falha ao realizar a devolução do item para o empréstimo {rent_id}. Verifique suas permissões ou o ID do empréstimo.")
 
            '''
            RentMediator().return_item(rent_id)
            return JSONResponse(
                content='Devolução realizada com sucesso',
                status_code=status.HTTP_201_CREATED
            )

        @self.router.get("/history")
        def get_history(token_verify=Depends(auth_admin)):
            '''
            ### Obter Histórico de Empréstimos

            Recupera o histórico completo de empréstimos no sistema.

            **Endpoint:** `GET rent/history`

            **Acesso:** Somente administradores autenticados.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna uma lista de todos os registros de empréstimos.
            - **401 Unauthorized**: Acesso não autorizado. Somente administradores podem acessar o histórico de empréstimos.
            - **403 Forbidden**: Falha na autenticação. O token de acesso fornecido não é válido.
            - **404 Not Found**: Não foram encontrados registros de empréstimos no sistema.
            - **409 Conflict**: O item está esgotado e não pode ser pego emprestado.


            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação de administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            response = requests.get("https://rentup.com/rent/history", headers=headers)
            if response.status_code == 200:
                historico_emprestimos = response.json()
                for emprestimo in historico_emprestimos:
                    print(emprestimo)
            else:
                print("Nenhum registro de empréstimo encontrado no sistema. Verifique suas permissões de administrador.")

            '''
            history = RentMediator().get_history()
            
            history_data = [{
                'id': item_data.id,
                'user': UserMediator().get_user_by_id(item_data.user_id).nome,
                'item': ItemMediator().get_item_by_id(item_data.item_id).nome_item,
                'data_emprestimo': str(item_data.data_emprestimo),
                'data_devolução': str(item_data.data_devolucao),
                'estado': item_data.estado, } for item_data in history]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=history_data
            )


        @self.router.get("/history-item")
        def get_history_by_item(item:str):
            '''
            ### Histórico de Empréstimos por Item

            Recupera o histórico de empréstimos filtrado pelo nome do item no sistema.

            **Endpoint:** `GET /rent/history-item?item={item}`

            **Acesso:** Somente usuários autenticados.

            **Parâmetros da Requisição:**
            - **item** (string): Nome do item para o qual deseja-se recuperar o histórico de empréstimos.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna uma lista de empréstimos filtrados pelo nome do item.
            - **403 Forbidden**: Acesso não autorizado. O usuário não está autenticado.
            - **404 Not Found**: Nenhum empréstimo encontrado para o item especificado.

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação do usuário
            headers = {"Authorization": "Bearer <token_do_usuario>"}

            # Nome do item para o qual deseja-se recuperar o histórico
            nome_do_item = "Item A"

            response = requests.get(f"https://rentup.com/rent/history-item?item={nome_do_item}", headers=headers)
            if response.status_code == 200:
                historico_emprestimos = response.json()
                for emprestimo in historico_emprestimos:
                    print(emprestimo)
            else:
                print(f"Nenhum empréstimo encontrado para o item {nome_do_item}. Verifique suas permissões ou o nome do item.")

            '''
            history_item = RentMediator().get_history_by_item(BaseItem(nome=item))

            if len(history_item) == 0:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"message": "Nenhum empréstimo encontrado para o item especificado."}
                )
            
            history_item_data = [{
                'id': item_data.id,
                'user': UserMediator().get_user_by_id(item_data.user_id).nome,
                'item': ItemMediator().get_item_by_id(item_data.item_id).nome_item,
                'data_emprestimo': str(item_data.data_emprestimo),
                'data_devolução': str(item_data.data_devolucao),
                'estado': item_data.estado, }for item_data in history_item]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"rents": history_item_data}
            )

        @self.router.get("/history-user")
        def get_history_by_user(user_email:str):
            '''
            ### Histórico de Empréstimos por Usuário

            Recupera o histórico de empréstimos filtrado pelo e-mail do usuário no sistema.

            **Endpoint:** `GET /rent/history-user?user_email={user_email}`

            **Acesso:** Somente usuários autenticados.

            **Parâmetros da Requisição:**
            - **user_email** (string): E-mail do usuário para o qual deseja-se recuperar o histórico de empréstimos.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna uma lista de empréstimos filtrados pelo e-mail do usuário.
            - **403 Forbidden**: Acesso não autorizado. O usuário não está autenticado.
            - **404 Not Found**: Nenhum empréstimo encontrado para o usuário especificado.

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação do usuário
            headers = {"Authorization": "Bearer <token_do_usuario>"}

            # E-mail do usuário para o qual deseja-se recuperar o histórico
            email_do_usuario = "usuario@example.com"

            response = requests.get(f"https://rentup.com/rent/history-user?user_email={email_do_usuario}", headers=headers)
            if response.status_code == 200:
                historico_emprestimos = response.json()
                for emprestimo in historico_emprestimos:
                    print(emprestimo)
            else:
                print(f"Nenhum empréstimo encontrado para o usuário {email_do_usuario}. Verifique suas permissões ou o e-mail do usuário.")

            '''
            history_user = RentMediator().get_history_by_user(user_email)
            history_user_data = [{
                'id': item_data.id,
                'user': UserMediator().get_user_by_id(item_data.user_id).nome,
                'item': ItemMediator().get_item_by_id(item_data.item_id).nome_item,
                'data_emprestimo': str(item_data.data_emprestimo),
                'data_devolução': str(item_data.data_devolucao),
                'estado': item_data.estado, }for item_data in history_user]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"rents": history_user_data}
            )

        @self.router.put("/update-status")
        def update_status(id_rent:int, stat:Status, token_verify=Depends(auth_admin)):
            '''
            ### Atualizar Status de Empréstimo

            Atualiza o status de um empréstimo no sistema.

            **Endpoint:** `PUT /rent/update_status?id_rent={id_rent}&stat={status}`

            **Acesso:** Somente administradores autenticados.

            **Parâmetros da Requisição:**
            - **id_rent** (string): ID único do empréstimo que terá seu status atualizado.
            - **status** (string): Novo status do empréstimo. Deve ser uma das seguintes opções do Enum `Status`: "APPROVED", "DISAPPROVED", "WAITING", "RETURNED".

            **Códigos de Resposta:**
            - **200 OK**: A atualização do status do empréstimo foi bem-sucedida.
            - **400 Bad Request**: A solicitação não atende aos requisitos (por exemplo, status inválido).
            - **401 Unauthorized**: Acesso não autorizado. O usuário não possui privilégios de administrador.
            - **403 Forbidden**: Acesso não autorizado. O usuário não está autenticado.
            - **404 Not Found**: Nenhum empréstimo com o ID especificado foi encontrado no sistema.

            **Exemplo de Uso:**
            ```python
            import requests

            # Token de autenticação do administrador
            headers = {"Authorization": "Bearer <token_do_administrador>"}

            # ID do empréstimo a ter o status atualizado
            id_do_emprestimo = "1234567890"

            # Novo status do empréstimo (por exemplo, "APPROVED", "DISAPPROVED", "WAITING", "RETURNED")
            novo_status = "APPROVED"

            response = requests.put(f"https://rentup.com/rent/update_status?id_rent={id_do_emprestimo}&stat={novo_status}", headers=headers)
            if response.status_code == 200:
                print(f"Status do empréstimo {id_do_emprestimo} atualizado para {novo_status} com sucesso.")
            else:
                print(f"Falha ao atualizar o status do empréstimo {id_do_emprestimo}. Verifique suas permissões ou o ID do empréstimo.")

            '''
            RentMediator().update_status(id_rent, stat)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Status atualizado com sucesso"}
            )
        
        
