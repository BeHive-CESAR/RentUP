from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .Status import Status
from infra.entities.rent import Rent as RentDB

class Rent(BaseModel):
    user: str
    itens: str
    rentDate: datetime
    returnDate: Optional[datetime]=None
    status: Status

    def to_banco(self):
        '''Metodo que tranforma o objeto Rent em um rent para o banco de dados'''
        data_insert = RentDB(
                    user_email=self.user, 
                    item_nome=self.itens.capitalize(),
                    data_emprestimo=self.rentDate,
                    data_devolucao=self.returnDate,
                    estado=self.status.name,
                )
        return data_insert
    