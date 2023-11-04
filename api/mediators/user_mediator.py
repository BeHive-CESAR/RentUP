
from datetime import datetime
from infra.repository.user_repository import UserRepository
from infra.entities.users import User

class UserMediator:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __validate_email(self, email: str):
        existing_user = self.user_repository.select_by_email(User(email=email))
        if existing_user:
            raise ValueError("Esse email já existe.")

    def __validate_password(self, password: str):
        if len(password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not any(char.isupper() for char in password):
            raise ValueError("É necessário ter uma letra maiúscula.")
        if not any(char.isdigit() for char in password):
            raise ValueError("É necessário ao menos 1 dígito.")
        if not any(char in '!@#$%^&*()_+,' for char in password):
            raise ValueError("É necessário ter um caractere especial.")

    def __validate_name(self, name: str):
        existing_user = self.user_repository.select(User(name=name))
        if existing_user:
            raise ValueError("Esse nome já existe.")

    def create_user(self, user: User):
        self.__validate_email(user.email)
        self.__validate_password(user.senha)
        self.__validate_name(user.nome)
        self.user_repository.insert(user)

    def get_users(self):
        return self.user_repository.select()

    def get_user_by_email(self, email: str):
        return self.user_repository.select_by_email(User(email=email))

    def edit_user(self, original_email: str, updated_user: User):
        original_user = self.get_user_by_email(original_email)
        if original_user.email != updated_user.email:
            self.__validate_email(updated_user.email)
        if original_user.name != updated_user.nome:
            self.__validate_name(updated_user.name)
        self.__validate_password(updated_user.password)
        self.user_repository.update(original_user, updated_user)

    def delete_user(self, email: str):
        user_to_delete = User(email=email)
        self.user_repository.delete(user_to_delete)
