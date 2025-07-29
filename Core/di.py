from aiogram import BaseMiddleware
from dependency_injector import containers, providers
from Services.UserDataService import UserService, UserRepository
from Services.SubjectService import SubjectRepository, SubjectService
from Services.UsersListsService import ListRepository, ListService
from Services.PrivilegeService import PrivilegeRepository, PrivilegeService
from Infrastructure.Database.db import DataBase

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(DataBase)

    session_provider = providers.Resource(db.provided.session_make)

    us_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService,repo = us_repo)

    sub_repo = providers.Factory(SubjectRepository)
    subject_service = providers.Factory(SubjectService, repo = sub_repo)

    list_repo = providers.Factory(ListRepository)
    list_service = providers.Factory(ListService, repo = list_repo)

    privilege_repo = providers.Factory(PrivilegeRepository)
    privilege_service = providers.Factory(PrivilegeService, repo = privilege_repo)


class DIMiddleware(BaseMiddleware):
    def __init__(self, container: Container):
        self.container = container

    async def __call__(self, handler, event, data):
        db = self.container.db()
        async with db.session_make() as session:
            user_repository = self.container.us_repo(session=session)
            subject_repository = self.container.sub_repo(session=session)
            list_repository = self.container.list_repo(session=session)
            privilege_repository = self.container.privilege_repo(session=session)

            user_service = self.container.user_service(repo = user_repository)
            subject_service = self.container.subject_service(repo=subject_repository)
            list_service = self.container.list_service(repo=list_repository)
            privilege_service = self.container.privilege_service(repo=privilege_repository)

            data['user_service'] = user_service
            data['list_service'] = list_service
            data['subject_service'] = subject_service
            data['privilege_service'] = privilege_service
            return await handler(event,data)

