from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from api.mediators.user_mediator import UserMediator, Users, UserAuth
from api.depends import auth_wrapper
import urllib.parse


class UsersController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post('/register')
        async def user_register(user: Users):
            UserMediator().create_user(user)
            return JSONResponse(
                content={'Registro': 'Sucesso'},
                status_code=status.HTTP_201_CREATED
            )
        
        @self.router.post('/login')
        async def user_login(user: UserAuth):

            auth_data = UserMediator().user_login(user=user)
            return JSONResponse(
                content=auth_data,
                status_code=status.HTTP_202_ACCEPTED
            )
        
        @self.router.get('/get-users')
        async def get_users(token_verify=Depends(auth_wrapper)):
            users_list = UserMediator().get_users()
            user_data = [{'nome': user.nome, 'email': user.email, 'contato': user.contato, 'role': user.papel} for user in users_list]
            return JSONResponse(
                content=user_data,
                status_code=status.HTTP_200_OK
            )
            

        @self.router.get('/get-user-by-name')
        async def get_user_by_name(nome:str ,token_verify=Depends(auth_wrapper)):
            nome = urllib.parse.unquote(nome)
            users_list = UserMediator().get_user_by_name(nome)
            user_data = [{'nome': user.nome, 'email': user.email, 'contato': user.contato, 'role': user.papel} for user in users_list]
            return JSONResponse(
                content= user_data,
                status_code=status.HTTP_200_OK
            )

        @self.router.put('/edit-user')
        async def edit_user(email:str, user:Users, token_verify=Depends(auth_wrapper)):
            UserMediator().edit_user(email, user)
            return JSONResponse(
                content={'Editado': 'Lucas'},
                status_code=status.HTTP_200_OK
            )

        @self.router.delete('/delete-user')
        async def user_delete(email:str, token_verify=Depends(auth_wrapper)):
            UserMediator().delete_user(email)
            return JSONResponse(
                content={'Deletado': 'Sucesso'},
                status_code=status.HTTP_201_CREATED
            )
