from fastapi import APIRouter
from api.entidades.Users import Users


class UsersController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post('/')
        async def teste(user: Users):
            return user