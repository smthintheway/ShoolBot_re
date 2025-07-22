from aiogram import Dispatcher
from dependency_injector import containers, providers
from Services.UserService import UserService, IUserRepository
from Services.SubjectService import ISubjectRepository, SubjectRepository
from Services.UsersListsService import IListRepository, ListRepository

class Container(containers.DeclarativeContainer):
    us_repo = providers.Singleton(IUserRepository)
    user_service = providers.Factory(UserService,repo = us_repo)

    sub_repo = providers.Singleton(ISubjectRepository)
    subject_service = providers.Factory(SubjectRepository, repo = sub_repo)

    list_repo = providers.Singleton(IListRepository)
    list_service = providers.Factory(ListRepository, repo = list_repo)

def setup_di(dp: Dispatcher):
    container = Container()
    dp['container'] = container