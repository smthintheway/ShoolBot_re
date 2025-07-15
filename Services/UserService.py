from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Infrastructure.Tables.Users import Users


class IUserRepository():
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_user(self, tg_id: int) -> Users | None:
        result = await self.session.execute(select(Users).filter(Users.tg_id == tg_id))
        await self.session.commit()
        return result.scalar()


    async def reg_or_update(self,user: dict) -> Users | None:
        try:
            old_user = await self.get_user(user['tg_id'])
            if old_user is None:
                new_user = Users(tg_id = user['tg_id'],
                                     username = user['username'],
                                     form = user['form'],
                                     group = user['group'],
                                     privileges = user['privileges'])
                self.session.add(new_user)
            else:
                old_user.username = user['username'] or old_user.username
                old_user.form = user['form'] or old_user.form
                old_user.group= user['group'] or old_user.group
                old_user.privileges = user['privileges'] or old_user.privileges

            await self.session.commit()
            return old_user

        except Exception as error:
            print(error)


class UserService:
    def __init__(self, repo: IUserRepository):
        self._repo = repo

    async def registration(self,user: dict) -> Users | None:
        try:
            return await self._repo.reg_or_update(user)
        except Exception as error:
            print(error)

    async def get_user_reg(self,tg_id: int):
        try:
            return await self._repo.get_user(tg_id)
        except Exception as error:
            print(error)

    async def get_user_info(self,tg_id: int) -> dict[str,int] | None:
        try:
            user = await self._repo.get_user(tg_id)
            data = {
                'username': user.username,
                'tg_id': user.tg_id,
                'form': user.form,
                'group': user.group,
                'privileges': user.privileges
            }
            return data
        except Exception as error:
            print(error)
