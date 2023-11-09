from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from .Status import Status

class Rent(BaseModel):
    user: EmailStr
    itens: str
    rentDate: datetime
    status: Status = Status.WAITING

class ReturnRent(Rent):
    returnDate: datetime