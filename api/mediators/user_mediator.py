import re
from datetime import datetime, timedelta
from fastapi import status
from decouple import config
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from api.entidades.Users import Users, User
from infra.repository.user_repository import UserRepository

class UserMediator:
    def __init__(self):
        self.user_repository = UserRepository()
        self.crypt_context = CryptContext(schemes=['sha256_crypt'])
        self.SECRET_KEY = config('SECRET_KEY')
        self.ALGORITHM = config('ALGORITHM')

    def __validate_email(self, email: str):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        existing_user = self.user_repository.select_by_email(email)
        if existing_user:
            raise ValueError("Esse email já existe.")
        if not re.search(regex, email):
            raise ValueError("Email invalido")

    def __validate_password(self, password: str):
        if len(password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not any(char.isupper() for char in password):
            raise ValueError("A senha deve ter uma letra maiúscula.")
        if not any(char.isdigit() for char in password):
            raise ValueError("A senha deve ter ao menos 1 dígito.")
        if not any(char in '!@#$%^&*()_+,' for char in password):
            raise ValueError("A senha deve ter um caractere especial.")

    def __validate_name(self, name: str):
        existing_user = self.user_repository.select(Users(name=name))
        if existing_user:
            raise ValueError("Esse nome já existe.")
        
        # Validar se o nome tem mais de 2 caracteres
        # O nome só pode ter letras e números
        # Pode ter mais de um usuario com o mesmo nome 

    def create_user(self, user: Users):
        self.__validate_email(user.email)
        self.__validate_password(user.password)
        # self.__validate_name(user.nome)

        user_db = User(
            nome=user.nome,
            email=user.email,
            senha=self.crypt_context.hash(user.password),
            papel=user.role.name
        )
        self.user_repository.insert(user_db)

    def get_users(self):
        return self.user_repository.select()

    def get_user_by_email(self, email: str):
        return self.user_repository.select_by_email(email)

    def edit_user(self, original_email: str, updated_user: Users):
        original_user = self.get_user_by_email(original_email)
        if original_user.email != updated_user.email:
            self.__validate_email(updated_user.email)
        if original_user.nome != updated_user.nome:
            self.__validate_name(updated_user.nome)
        self.__validate_password(updated_user.password)

        self.user_repository.update(original_user, updated_user.to_banco())

    def delete_user(self, email: str):
        user_to_delete = User(email=email)
        self.user_repository.delete(user_to_delete)

    def user_login(self, user:Users, expires_in:int=60):
        user_on_db = self.get_user_by_email(user.email)

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email ou senha invalido'
            )
        if not self.crypt_context.verify(user.password, user_on_db.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email ou senha invalido'
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': user.email,
            'exp': exp
        }

        acess_token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return {
            'acess_token': acess_token,
            'exp': exp.isoformat()
        }
    
    def verify_token(self, acess_token):
        try:
            data = jwt.decode(acess_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token de acesso invalido'
            )
        
        user_on_db = self.get_user_by_email(data['sub'])

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token de acesso invalido'
            )
        
