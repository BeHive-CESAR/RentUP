from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api.mediators.user_mediator import UserMediator, Users, UserAuth


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
                status_code=status.HTTP_200_OK
            )
