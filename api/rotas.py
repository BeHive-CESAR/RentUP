from fastapi import APIRouter
from .controllers import ItemController as item
from .controllers import UsersController as user

router = APIRouter()

router.include_router(item.router, prefix="/item")
router.include_router(user.router, prefix="/user")

