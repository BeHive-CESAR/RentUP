from pydantic import BaseModel
from .Item import Item
from .Role import Role
from datetime import datetime
from .Users import Users
from .RentStatus import Status

class Rent(BaseModel):
    user: Users
    itens: Item
    rentDate: datetime
    returnDate: datetime
    status: Status

    # isso ta difernete das outras entidades, ta desatualizado?
    class Rent:
        def __init__(self, user: Users, itens: Item, rent_date: datetime, return_date: datetime):
            self.user = user
            self.itens = itens
            self.rent_date = rent_date
            self.return_date = return_date
    
    # não sei se era pra criar esse
    def to_banco(self):
        '''Metodo que tranforma o objeto Rent em um rent para o banco de dados'''
        data_insert = Rent(
                    user=self.user, # Como puxar o user itens e status
                    itens=self.itens,
                    rentdate=self.rentDate,
                    returndate=self.returnDate,
                    status=self.status.name,

                )
        return data_insert
    