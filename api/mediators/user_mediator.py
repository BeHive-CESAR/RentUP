import re
from datetime import datetime, timedelta
from fastapi import status
from decouple import config
import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import ProgrammingError, IntegrityError
from fastapi.exceptions import HTTPException
from api.entidades.Users import Users, UserAuth, UserCreation
from infra.repository.user_repository import UserRepository, User
from api.entidades.Role import Role


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
        
        if len(name) < 3:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username deve ter pelo menos 3 digitos")
        
        if len(name) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username deve ter no máximo 50 caracteres")
        
        if not re.match(r"^[a-zA-ZÀ-ÿ.\s]+$", name): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username deve conter apenas letras e espaços")
    
    def __validate_number(self, number:str):
        '''Método responsavel por validar o numero de telefone
        
        Keyword arguments:

        number -- str que será validado 
        '''
        if len(number) < 9:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de telefone deve ter pelo menos 9 digitos")
        
        if len(number) > 11:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de telefone deve ter no máximo 11 digitos")
        
        if len(number) == 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inclua o DDD no número de telefone")
        
        if not re.match(r"^[0-9]+$", number): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de telefone deve conter apenas números")

    def create_user(self, user:UserCreation):
        '''Método responsavel por, após validações, criar um usuario no banco de dados
        com senha criptografada
        
        Keyword arguments:

        user - objeto do tipo Users que será gravado no banco
        '''

        self.__validate_email(user.email)
        self.__validate_password(user.password)
        self.__validate_name(user.nome)
        self.__validate_number(user.contato)

        user_db = User(
            nome=user.nome,
            email=user.email,
            senha=self.crypt_context.hash(user.password),
            contato=user.contato,
            papel=Role.USER.name
        )
        try:
            self.user_repository.insert(user_db)
        except IntegrityError:
            raise HTTPException(
                detail='Número de telefone já cadastrado',
                status_code=status.HTTP_409_CONFLICT
            )
        

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
    
    def get_user_by_id(self, id:int):
        '''Retorna um usuario especifico a partir do id
        
        Keyword arguments:

        id -- int para busca do usuario
        '''
        return self.user_repository.select_user_by_id(id)

    def edit_user(self, original_email:str, updated_user:Users):
        '''Realiza a validação do email e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa o usuario e edita-o. Caso não retorna uma mensagem de erro

        Keyword arguments:

        original_email -- email que será buscado e editado
        
        updated_user -- Objeto do tipo Users que deverá possuir os novos dados para substituir o original_email no banco
        '''
        original_user = self.get_user_by_email(original_email)

        if original_user is None:
            raise HTTPException(
                detail='Usuário não encontrado',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if original_user.nome != updated_user.nome:
            self.__validate_name(updated_user.nome)

        if original_user.email != updated_user.email:
            self.__validate_email(updated_user.email)
        
        self.__validate_password(updated_user.password)

        novo_user = User(
            nome=updated_user.nome,
            email=updated_user.email,
            senha=self.crypt_context.hash(updated_user.password),
            contato=updated_user.contato,
            papel=updated_user.role.name
        )

        self.user_repository.update(original_user, novo_user)
    
    def edit_user_role(self, email:str, role:Role):
        '''Realiza a validação do email e verifica se o mesmo existe no banco. Caso esteja tudo OK acessa o usuario e edita-o. Caso não retorna uma mensagem de erro

        Keyword arguments:

        email -- email que será buscado e editado
        
        role -- Objeto do tipo Role que deverá possuir o novo cargo para substituir no usuario
        '''
        user = self.get_user_by_email(email)

        if user is None:
            raise HTTPException(
                detail='Usuário não encontrado',
                status_code=status.HTTP_404_NOT_FOUND
            )

        self.user_repository.update_role(user, role)

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
        
        try:
            self.user_repository.delete(user_to_delete)
        except ProgrammingError:
            raise HTTPException(
                detail='Não foi possível deletar o usuário pois ele possui itens emprestados',
                status_code=status.HTTP_409_CONFLICT
            )

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
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token'
            )
    
    def verify_admin(self, token):
        '''Metodo responsavel por verificar se o token enviado é válido e se o usuario possui permissão de administrador'''
        payload = self.verify_token(token)
        user = self.get_user_by_email(payload)
        if user.papel != Role.ADMINISTRATOR.name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Você não possui permissão para acessar esse recurso'
            )
