from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Infrastructure.Tables.Users import Users
from abc import ABC,abstractmethod

class IListRepository(ABC):
    @abstractmethod
    async def get_user_lists(self,condition = None) -> dict[str,int]: ...



class ListRepository(IListRepository):
    def __init__(self,session: AsyncSession):
        self.session = AsyncSession

