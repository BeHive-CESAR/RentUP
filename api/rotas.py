from fastapi import APIRouter, Depends
from .controllers.ItemController import ItemController as Item
from .controllers.UsersController import UsersController as User
from .depends import token_verifier

router = APIRouter()

router.include_router(Item().router, prefix="/item", dependencies=[Depends(token_verifier)])
router.include_router(User().router, prefix="/user")

