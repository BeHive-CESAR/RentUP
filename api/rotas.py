from fastapi import APIRouter, Depends
from .controllers.ItemController import ItemController as Item
from .controllers.UsersController import UsersController as User
from .depends import auth_wrapper

router = APIRouter()

router.include_router(Item().router, prefix="/item", dependencies=[Depends(auth_wrapper)], tags=['Itens'])
router.include_router(User().router, prefix="/user", tags=['Users'])

