from enum import Enum

class Status(Enum):
    '''Vai indicar a aprovação do pedido de emprestimo'''
    APPROVED = "APROVED"
    DISAPPROVED = "DISAPROVED"
    WAITING = "WAITING"