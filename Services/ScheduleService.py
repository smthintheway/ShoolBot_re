from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from Infrastructure.Database.Tables.Schedule import Schedule
from abc import ABC,abstractmethod


class IScheduleRepository(ABC):
    @abstractmethod
    async def add_week(self, new_schedule: str) -> Schedule: ...

    @abstractmethod
    async def update_week(self, new_schedule: str) -> Schedule:

    @abstractmethod
    async def ask_shedule(self,form)->Schedule:...


class ScheduleRepository(IScheduleRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def addweekday(self,weekday: str ,new_schedule: str) -> Schedule:
