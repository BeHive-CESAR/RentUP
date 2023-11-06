from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.mediators.user_mediator import UserMediator, Users
from api.depends import auth_wrapper


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
        async def user_login(user: Users):

            auth_data = UserMediator().user_login(user=user)
            return JSONResponse(
                content=auth_data,
                status_code=status.HTTP_200_OK
            )

        @self.router.get('/unprotected')
        async def unprotected():
            return { 'hello': 'world' }
        
        @self.router.get('/protected')
        def protected(username=Depends(auth_wrapper)):
            return { 'name': username }