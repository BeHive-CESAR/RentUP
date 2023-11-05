from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.mediators.user_mediator import UserMediator, Users
from api.entidades.Role import Role
from fastapi.security import OAuth2PasswordRequestForm


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
        async def user_login(request_form_user: OAuth2PasswordRequestForm = Depends()):
            
            user = Users(
                email=request_form_user.username,
                password=request_form_user.password,
            )

            auth_data = UserMediator().user_login(user=user)
            return JSONResponse(
                content=auth_data,
                status_code=status.HTTP_200_OK
            )