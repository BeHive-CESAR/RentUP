from pydantic import BaseModel
from .Item import Item
from .Role import Role
from datetime import datetime
from .Users import Users
class Rent(BaseModel):
    user: Users
    itens: Item
    rent_date: datetime
    return_date: datetime

    class Rent:
        def __init__(self, user: Users, itens: Item, rent_date: datetime, return_date: datetime):
            self.user = user
            self.itens = itens
            self.rent_date = rent_date
            self.return_date = return_date
    