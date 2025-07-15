from aiogram import Dispatcher
from dependency_injector import containers, providers
from Services.UserService import UserService, IUserRepository

class Container(containers.DeclarativeContainer):
    us_repo = providers.Singleton(IUserRepository)
    user_service = providers.Factory(UserService,repo = us_repo)

def setup_di(dp: Dispatcher):
    container = Container()
    dp['container'] = container