from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Infrastructure.Database.Tables.Users import Users
from abc import ABC,abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    async def get_user(self, tg_id) -> Users|None: ...

    @abstractmethod
    async def reg_or_update(self,tg_id) -> Users: ...


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, tg_id: int) -> Users | None:
        result = await self.session.execute(select(Users).filter(Users.tg_id == tg_id))
        return result.scalar()


    async def reg_or_update(self,user: dict) -> Users | None:
            existing = await self.get_user(user['tg_id'])
            if existing is None:
                new_user = Users(tg_id = user['tg_id'],
                                     username = user['username'],
                                     form = user['form'],
                                     group = user['group'],
                                     privileges = user['privileges'])
                self.session.add(new_user)
            else:
                existing.username = user['username'] or existing.username
                existing.form = user['form'] or existing.form
                existing.group= user['group'] or existing.group
                existing.privileges = user['privileges'] or existing.privileges

            await self.session.commit()
            return existing


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def registration(self,user: dict) -> Users | None:
        return await self._repo.reg_or_update(user)


    async def get_user_reg(self,tg_id: int):
            return await self._repo.get_user(tg_id)


    async def get_user_info(self,tg_id: int) -> dict[str,int] | None:
            user = await self._repo.get_user(tg_id)
            if user is None:
                return None
            return await User_info_DTO.user_info_show(user = user)


class User_info_DTO:
    @staticmethod
    async def user_info_show(user: Users) -> dict[str, int]:
        return {
                'username': user.username,
                'tg_id': user.tg_id,
                'form': user.form,
                'group': user.group,
                'privileges': user.privileges
            }