from pydantic import BaseModel
from .Item import Item
from .Role import Role
from datetime import datetime
from .Users import Users
from .Status import Status

class Rent(BaseModel):
    user: Users
    itens: Item
    rentDate: datetime
    returnDate: datetime
    status: Status

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
    