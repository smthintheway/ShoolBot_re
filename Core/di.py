from aiogram import Dispatcher
from dependency_injector import containers, providers
from Services.UserService import UserService, IUserRepository
from Services.SubjectService import ISubjectRepository, SubjectRepository

class Container(containers.DeclarativeContainer):
    us_repo = providers.Singleton(IUserRepository)
    user_service = providers.Factory(UserService,repo = us_repo)

    sub_repo = providers.Singleton(ISubjectRepository)
    subject_service = providers.Factory(SubjectRepository, repo = sub_repo)

def setup_di(dp: Dispatcher):
    container = Container()
    dp['container'] = container