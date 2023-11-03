from infra.repository.user_repository import User
from api.entidades.Users import User
class UserMediator:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def validate_email(self, email, user:User):
        if self.user_repository.select_by_email(email):
            raise ValueError("Esse email ja existe.")

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not any(char.isupper() for char in password):
            raise ValueError("É necessario ter uma letra maiuscula.")
        if not any(char.isdigit() for char in password):
            raise ValueError("É necessario ao menos 1 digito.")
        if not any(char in '!@#$%^&*()_+,' for char in password):
            raise ValueError("É necessario ter um caracter especial.")

    def validate_name(self, name):
        if self.user_repository.select(name):
            raise ValueError("Esse nome ja existe.")

    #def create_user(self, user):

   # def get_users(self):

    #def get_user(self, user_id):

    #def edit_user(self, original_user, updated_user):

  #  def delete_user(self, user_id):
