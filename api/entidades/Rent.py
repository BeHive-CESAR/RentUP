from pydantic import BaseModel
from .Item import Item
from datetime import datetime
from .Users import Users
from .Status import Status
from typing import Optional

class Rent(BaseModel):
    user: Users
    itens: Item
    rentDate: datetime
    returnDate: Optional[datetime]=None
    status: Status

    def to_banco(self):
        '''Metodo que tranforma o objeto Rent em um rent para o banco de dados'''
        data_insert = Rent(
                    user_email=self.user, 
                    item_nome=self.itens,
                    data_emprestimo=self.rentDate,
                    data_devolucao=self.returnDate,
                    estado=self.status.name,
                    
                )
        return data_insert
    