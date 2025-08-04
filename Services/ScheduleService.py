from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from Infrastructure.Database.Tables.Schedule import Schedule
from abc import ABC,abstractmethod


class IScheduleRepository(ABC):
    @abstractmethod
    async def get_shelude(self, form: str) -> Schedule|None: ...

    @abstractmethod
    async def add_week(self, new_schedule: str, form: str) -> Schedule: ...

    @abstractmethod
    async def update_week(self, new_schedule: str, form: str) -> Schedule: ...

    @abstractmethod
    async def ask_week_shedule(self, form: str)->Schedule: ...

    @abstractmethod
    async def ask_day_schedule(self, form: str, day: str)->Schedule: ...


class ScheduleRepository(IScheduleRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_shelude(self, form) -> Schedule:
        result = self.session.execute(select(Schedule).where(Schedule.form == form))
        if result is not None:
            return result
    
    async def ask_day_schedule(self,day: str, form: str) -> Schedule:
        result = await get_schelude(form)
        result = result[f'{day}']
        return result

    
    