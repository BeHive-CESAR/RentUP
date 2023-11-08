from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from api.mediators.user_mediator import UserMediator, Users, UserAuth
from api.depends import auth_wrapper
import urllib.parse


class UsersController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post('/register')
        async def user_register(user: Users):
            '''
            ### Endpoint de Registro de Usuário

            Registra um novo usuário no sistema com os seguintes detalhes:

            **Endpoint:** `POST /user/register`

            **Parâmetros da Requisição:**
            - **email** (string): O endereço de e-mail do usuário.
            - **password** (string): A senha do usuário.
            - **nome** (string): O nome completo do usuário.
            - **contato** (string): O número de telefone do usuário.
            - **cargo** (string): O cargo ou função do usuário.

            **Códigos de Resposta:**
            - **201 Created**: O registro do usuário foi bem-sucedido. O usuário foi criado com sucesso.
            - **400 Bad Request**: A solicitação de registro não atende aos requisitos (por exemplo, campos em branco, formato de e-mail inválido).
            - **409 Conflict**: Conflito de dados. O endereço de e-mail já está em uso por outro usuário.

            **Exemplo de Uso:**
            ```python
            import requests

            data = {
                "email": "novo_usuario@example.com",
                "password": "senha_segura",
                "nome": "Novo Usuário",
                "contato": "+1234567890",
                "cargo": "USER"
            }

            response = requests.post("https://rentup.com/user/register", data=data)
            if response.status_code == 201:
                print("Novo usuário registrado com sucesso.")
            else:
                print("Falha no registro. Verifique os dados fornecidos ou o endereço de e-mail já está em uso.")

            '''
            UserMediator().create_user(user)
            return JSONResponse(
                content={'Registro': 'Sucesso'},
                status_code=status.HTTP_201_CREATED
            )
        
        @self.router.post('/login')
        async def user_login(user: UserAuth):
            '''
            ### Endpoint de Login

            Autentica um usuário no sistema por meio de email e senha.

            **Endpoint:** `POST /user/login`

            **Parâmetros da Requisição:**
            - **email** (string): O endereço de e-mail do usuário.
            - **password** (string): A senha do usuário.

            **Códigos de Resposta:**
            - **200 OK**: A autenticação foi bem-sucedida. O usuário está autenticado e recebe um token de acesso.
            - **401 Unauthorized**: Falha na autenticação. As credenciais fornecidas são inválidas.

            **Exemplo de Uso:**
            ```python
            import requests

            data = {
                "email": "usuario@example.com",
                "password": "senha_segura"
            }

            response = requests.post("https://rentup.com/user/login", data=data)
            if response.status_code == 200:
                token = response.json()["token"]
                print(f"Usuário autenticado com sucesso. Token de acesso: {token}")
            else:
                print("Falha na autenticação. Verifique suas credenciais.")

            '''

            auth_data = UserMediator().user_login(user=user)
            return JSONResponse(
                content=auth_data,
                status_code=status.HTTP_200_OK
            )
        
        @self.router.get('/get-users')
        async def get_users(token_verify=Depends(auth_wrapper)):
            """
            ### Lista de Usuários Cadastrados

            Retorna uma lista de todos os usuários cadastrados no sistema.

            **Endpoint:** `GET /user/get-users`

            **Parâmetros da Requisição:**
            - Nenhum.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna uma lista de todos os usuários cadastrados.
            - **404 Not Found**: Não foram encontrados usuários no sistema.

            **Exemplo de Uso:**
            ```python
            import requests

            response = requests.get("https://rentup.com/user/get-users")
            if response.status_code == 200:
                usuarios = response.json()
                for usuario in usuarios:
                    print(usuario)
            else:
                print("Nenhum usuário encontrado no sistema.")

            """
            users_list = UserMediator().get_users()
            user_data = [{'nome': user.nome, 'email': user.email, 'contato': user.contato, 'role': user.papel} for user in users_list]
            if len(users_list) == 0:
                return JSONResponse(
                content=user_data,
                status_code=status.HTTP_404_NOT_FOUND
                )
            return JSONResponse(
                content=user_data,
                status_code=status.HTTP_200_OK
                )
            

        @self.router.get('/get-user-by-name')
        async def get_user_by_name(nome:str ,token_verify=Depends(auth_wrapper)):
            '''
            ### Consultar Usuário por Nome

            Recupera informações de um usuário específico com base no seu nome.

            **Endpoint:** `GET /user/get-user-by-name?nome={nome}`

            **Parâmetros da Requisição:**
            - **nome** (string): O nome do usuário que deseja consultar.

            **Códigos de Resposta:**
            - **200 OK**: A solicitação foi bem-sucedida. Retorna informações do usuário com o nome correspondente.
            - **404 Not Found**: Nenhum usuário com o nome especificado foi encontrado no sistema.

            **Exemplo de Uso:**
            ```python
            import requests

            nome_do_usuario = "NomeUsuario"

            response = requests.get(f"https://rentup.com/user/get-user-by-name?nome={nome_do_usuario}")
            if response.status_code == 200:
                usuario = response.json()
                print(f"Informações do usuário {nome_do_usuario}:{usuario}")
            else:
                print(f"Usuário com o nome {nome_do_usuario} não encontrado no sistema.")
            '''
            nome = urllib.parse.unquote(nome)
            users_list = UserMediator().get_user_by_name(nome)
            user_data = [{'nome': user.nome, 'email': user.email, 'contato': user.contato, 'role': user.papel} for user in users_list]
            if len(users_list) == 0:
                return JSONResponse(
                    content=user_data,
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return JSONResponse(
                content= user_data,
                status_code=status.HTTP_200_OK
            )

        @self.router.put('/edit-user')
        async def edit_user(email:str, user:Users, token_verify=Depends(auth_wrapper)):
            '''
            ### Editar Usuário por Email

            Edita as informações de um usuário com base no seu endereço de e-mail.

            **Endpoint:** `PUT /user/edit-user?email={email}`

            **Parâmetros da Requisição:**
            - **email** (string): O endereço de e-mail do usuário que deseja editar.
            - **email** (string): Novo endereço de e-mail.
            - **password** (string): Nova senha do usuário.
            - **nome** (string): Novo nome do usuário.
            - **contato** (string): Novo número de telefone do usuário.
            - **cargo** (string): Novo cargo ou função do usuário.

            **Códigos de Resposta:**
            - **200 OK**: A edição do usuário foi bem-sucedida. As informações do usuário foram atualizadas com sucesso.
            - **404 Not Found**: Nenhum usuário com o email especificado foi encontrado no sistema.

            **Exemplo de Uso:**
            ```python
            import requests

            email_do_usuario = "usuario@example.com"
            novos_dados = {
                "password": "nova_senha_segura",
                "email": "novo_email@example.com",
                "nome": "Novo Nome",
                "contato": "+9876543210",
                "cargo": "User"
            }

            response = requests.put(f"https://exemplo.com/user/edit-user?email={email_do_usuario}", data=novos_dados)
            if response.status_code == 200:
                print(f"Informações do usuário com o email {email_do_usuario} foram atualizadas com sucesso.")
            else:
                print(f"Nenhum usuário com o email {email_do_usuario} encontrado para edição.")
            '''
            UserMediator().edit_user(email, user)
            return JSONResponse(
                content={'Edição bem sucedida': 'Sucesso'},
                status_code=status.HTTP_200_OK
            )

        @self.router.delete('/delete-user')
        async def user_delete(email:str, token_verify=Depends(auth_wrapper)):
            '''
            ### Excluir Usuário por Email

            Exclui um usuário com base no seu endereço de e-mail.

            **Endpoint:** `DELETE /user/delete-user?email={email}`

            **Parâmetros da Requisição:**
            - **email** (string): O endereço de e-mail do usuário que deseja excluir.

            **Códigos de Resposta:**
            - **204 No Content**: A exclusão do usuário foi bem-sucedida. O usuário com o email especificado foi removido do sistema.
            - **404 Not Found**: Nenhum usuário com o email especificado foi encontrado no sistema.

            **Exemplo de Uso:**
            ```python
            import requests

            email_do_usuario = "usuario@example.com"

            response = requests.delete(f"https://rentup.com/user/delete-user?email={email_do_usuario}")
            if response.status_code == 204:
                print(f"Usuário com o email {email_do_usuario} foi excluído com sucesso.")
            else:
                print(f"Nenhum usuário com o email {email_do_usuario} encontrado para exclusão.")

            '''
            UserMediator().delete_user(email)
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT
            )
        
