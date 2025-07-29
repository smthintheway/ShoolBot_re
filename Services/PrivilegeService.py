import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Infrastructure.Database.Tables.Users import Users
from abc import ABC,abstractmethod

class IPrivilegeRepository(ABC):
    @abstractmethod
    async def privilege_update(self, privilege_to_update: str, user_to_update: int|str) -> Users: ...


class PrivilegeRepository(IPrivilegeRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def privilege_update(self, privilege_to_update: str, user_to_update: int|str) -> Users:
        if isinstance(user_to_update, int):
            user_to_update = await self.session.execute(select(Users.tg_id).where(Users.tg_id == user_to_update))
        elif isinstance(user_to_update, str):
            user_to_update = await self.session.execute(select(Users.username).where(Users.username == user_to_update))
        user_to_update = user_to_update.scalar()
        user_to_update.privileges = privilege_to_update
        return user_to_update


class PrivilegeService:
    def __init__(self,repo: PrivilegeRepository):
        self._repo = repo
        with open('Core/settings.json') as f:
            self.privileges = json.load(f)['Privileges']

    async def add_new_admin(self,user_to_update: int|str) -> Users:
        result = await self._repo.privilege_update(privilege_to_update=self.privileges[1],
                                          user_to_update=user_to_update)
        return result

    async def add_new_headman(self,user_to_update: int|str) -> Users:
        result = await self._repo.privilege_update(privilege_to_update=self.privileges[2],
                                          user_to_update=user_to_update)
        return result

    async def add_new_headman_helper(self,user_to_update: int|str) -> Users:
        result = await self._repo.privilege_update(privilege_to_update=self.privileges[3],
                                          user_to_update=user_to_update)
        return result