import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import  or_
from Infrastructure.Database.Tables.Users import Users
from abc import ABC,abstractmethod

class IListRepository(ABC):
    @abstractmethod
    async def get_user_list(self,form: str, group: str, privilege: str): ...



class ListRepository(IListRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_user_list(self,form: str | None, group: str | None, privilege: str | None):
        query = select(Users)
        with open('Core/settings.json') as f:
            config = json.load(f)

        if form is not None:
            query = query.where(Users.form == form)
        if privilege  is not None:
            if privilege == config['Privileges'][1]:
                query = query.where(or_(Users.privileges == privilege, Users.privileges == config['Privileges'][0]))
            else:
                query = query.where(Users.privileges == privilege)
        if group is not None:
            query = query.where(Users.group in '1 0')

        result = await self.session.execute(query)
        return result.scalars().all()

class ListService:
    def __init__(self, repo: ListRepository):
        self._repo = repo

    async def get_privilege_list(self,form,privilege):
        result = await self._repo.get_user_list(form = form, privilege = privilege, group = None)
        return result

    async def get_classmates_list(self,form):
        result = await self._repo.get_user_list(form = form, group = None, privilege = None)
        return result