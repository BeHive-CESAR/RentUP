from fastapi import APIRouter, Depends
from .controllers.ItemController import ItemController as Item
from .controllers.UsersController import UsersController as User
from .controllers.RentController import RentController as Rent
from .depends import auth_wrapper

router = APIRouter()

router.include_router(Item().router, prefix="/item", dependencies=[Depends(auth_wrapper)], tags=['Itens'])
router.include_router(User().router, prefix="/user", tags=['Users'])
router.include_router(Rent().router, prefix="/rent", dependencies=[Depends(auth_wrapper)], tags=['Rent'])

