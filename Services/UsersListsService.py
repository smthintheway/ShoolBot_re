from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Infrastructure.Tables.Users import Users
from abc import ABC,abstractmethod

class IListRepository(ABC):
    @abstractmethod
    async def get_user_lists(self,condition) -> Users: ...


class ListRepository(IListRepository):
    def __init__(self,session: AsyncSession):
        self.session = AsyncSession

    async def get_privilege_lists(self,privilege, form = 0 )-> Users:
        result = await self.session.execute(select(Users).filter(Users.privileges == privilege and Users.form == form))
        return result.scalar()


class ListService:
    def __init__(self, repo: ListRepository):
        self._repo = repo

    async def get_privilege_list(self,form,privilege) -> list:
        result = await self._repo.get_user_lists(f'Users.form == {form} and Users.privileges == {privilege}')
        return result

    async def get_classmates_list(self,form) -> list:
        result = await self._repo.get_user_lists(f'Users.form == {form}')
        return result

    async def get_everybody_list(self) -> list:
        result = await self._repo.get_user_lists(None)
        return result