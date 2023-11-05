from api.mediators.rent_mediator import Rent, RentMediator, datetime, Item
from api.entidades.Users import Users, Role
from api.entidades.Status import Status
from api.mediators.user_mediator import UserMediator, UserRepository

item = Item(nome='Arduino')
user = Users(nome='Lucas', email='lgbs2@cesar.com', password='Luquinhas', role=Role.USER)

rent = Rent(itens=item.nome, rentDate=datetime.now(), user=user.email, status=Status.WAITING).to_banco()

usermed = UserMediator()

# print(usermed.get_user_by_email(user.email))
# print(usermed.__validate_email(email='lucas'))

# usermed.create_user(user)
print(usermed.create_user(user))

# print(UserRepository().select_by_email(user))


# CREATE_USER FUNCIONANDO
# __VALIDATE_NAME NÃO FAZ SENTIDO
# __VALIDATE_PASSWORD FUNCIONANDO
# __VALIDATE_EMAIL FUNCIONANDO
# GET_USERS FUNCIONANDO
# GET_USER_BY_EMAIL FUNCIONANDO
# EDIT_USER FUNCIONANDO
# DELETE_USER FUNCIONANDO