from fastapi import APIRouter
from .controllers.ItemController import ItemController as Item
from .controllers.UsersController import UsersController as User

router = APIRouter()

router.include_router(Item().router, prefix="/item")
router.include_router(User().router, prefix="/user")

