from enum import Enum

class Role(Enum):
    '''Enum responsavel por identificar qual será o papel do User'''
    ADMINISTRATOR = "ADMINISTRATOR"
    USER = "USER"