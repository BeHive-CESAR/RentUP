import re
from datetime import datetime, timedelta
from fastapi import status
from decouple import config
import jwt
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from api.entidades.Users import Users, User, UserAuth
from infra.repository.user_repository import UserRepository


class UserMediator:
    '''Classe responsavel por fazer o intermedio entre os endpoints e o repository'''
    def __init__(self):
        self.user_repository = UserRepository()
        self.crypt_context = CryptContext(schemes=['sha256_crypt'])
        self.SECRET_KEY = config('SECRET_KEY')
        self.ALGORITHM = config('ALGORITHM')

    def __validate_email(self, email:str):
        ''' Método responsavel por validar email

        Keyword arguments:

        email -- str que será validado
        '''
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,}$'
        existing_user = self.user_repository.select_by_email(email)
        if existing_user:
            raise HTTPException(
                detail="Esse email já existe.",
                status_code=status.HTTP_409_CONFLICT
            )
        if not re.search(regex, email):
            raise HTTPException(
                detail="Email invalido",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        return False

    def __validate_password(self, password:str):
        '''Método responsavel por validar a senha
        
        Keyword arguments:

        password -- str que será validada
        '''
        if len(password) < 8:
            raise HTTPException(
                detail="A senha deve ter pelo menos 8 caracteres.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not any(char.isupper() for char in password):
            raise HTTPException(
                detail="A senha deve ter uma letra maiúscula.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not any(char.isdigit() for char in password):
            raise HTTPException(
                detail="A senha deve ter ao menos 1 dígito.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not any(char in '!@#$%^&*()_+,' for char in password):
            raise HTTPException(
                detail="A senha deve ter um caractere especial.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def __validate_name(self, name:str):
        '''Método responsavel por validar o nome
        
        Keyword arguments:

        name -- str que será validado
        '''
        existing_user = self.user_repository.select(Users(name=name))
        if existing_user:
            raise ValueError("Esse nome já existe.")
        
        # Validar se o nome tem mais de 2 caracteres
        # O nome só pode ter letras e números
        # Pode ter mais de um usuario com o mesmo nome 

    def create_user(self, user:Users):
        '''Método responsavel por, após validações, criar um usuario no banco de dados
        com senha criptografada
        
        Keyword arguments:

        user - objeto do tipo Users que será gravado no banco
        '''

        validate_email = self.__validate_email(user.email)
        validate_password = self.__validate_password(user.password)
        # self.__validate_name(user.nome)

        user_db = User(
            nome=user.nome,
            email=user.email,
            senha=self.crypt_context.hash(user.password),
            contato=user.contato,
            papel=user.role.name
        )
        self.user_repository.insert(user_db)
        

    def get_users(self):
        '''Retorna todos os usuarios cadastrados no banco'''
        return self.user_repository.select()

    def get_user_by_email(self, email:str):
        '''Retorna um usuario especifico a partir do email
        
        Keyword arguments:

        email -- str para busca do usuario
        '''
        return self.user_repository.select_by_email(email)
    
    def get_user_by_name(self, nome:str):
        '''Retorna um usuario especifico a partir do nome
        
        Keyword arguments:

        nome -- str para busca do usuario
        '''
        return self.user_repository.select_by_name(nome)

    def edit_user(self, original_email:str, updated_user:Users):
        '''Realiza a validação do email e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa o usuario e edita-o. Caso não retorna uma mensagem de erro

        Keyword arguments:

        original_email -- email que será buscado e editado
        
        updated_user -- Objeto do tipo Users que deverá possuir os novos dados para substituir o original_email no banco
        '''
        original_user = self.get_user_by_email(original_email)
        if original_user.email != updated_user.email:
            self.__validate_email(updated_user.email)
        if original_user.nome != updated_user.nome:
            self.__validate_name(updated_user.nome)
        self.__validate_password(updated_user.password)

        self.user_repository.update(original_user, updated_user.to_banco())

    def delete_user(self, email:str):
        '''Metodo responsavel por deletar um user do banco de dados

        Keyword arguments:

        email -- str que representa o email do usuario que será deletado
        '''
        user_to_delete = self.get_user_by_email(email)
        if user_to_delete is None:
            raise HTTPException(
                detail='Usuário não encontrado',
                status_code=status.HTTP_404_NOT_FOUND
            )
        self.user_repository.delete(user_to_delete)

    def user_login(self, user:UserAuth, expires_in:int=5):
        '''Metodo responsavel por fazer a autenticação do usuario e retornar um token de acesso e os dados do usuario logado
        
        Keyword arguments:

        user -- Objeto do tipo UserAuth que será autenticado
        '''
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

        exp = datetime.utcnow() + timedelta(hours=expires_in)

        payload = {
            'exp': exp,
            'iat': datetime.utcnow(),
            'sub': user.email
        }

        return {'token': jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM),
                'username': user_on_db.nome, 'access':user_on_db.papel}
    
    def verify_token(self, token):
        '''Metodo responsavel por verificar se o token enviado é válido'''
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Signature has expired'
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token'
            )
