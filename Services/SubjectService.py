from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from Infrastructure.Database.Tables.Subjects import Subjects
from abc import ABC,abstractmethod
import datetime

class ISubjectRepository(ABC):
    @abstractmethod
    async def add_or_update_note(self,subject_name, form, editor, timestamp, comment, hw_type, content , group) -> Subjects: ...

    @abstractmethod
    async def get_subject_task(self, subject_name, form, group) -> Subjects: ...

class SubjectRepository(ISubjectRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_subject_task(self,subject_name, form, group):
        condition = and_(Subjects.subject_name == subject_name,
                         Subjects.form == form,
                         or_(Subjects.group == group , Subjects.group == '0'))
        result = await self.session.execute(select(Subjects).where(condition))
        return result.scalars().first()

    async def add_or_update_note(self,subject_name, form, editor, timestamp, comment, hw_type, content , group) -> Subjects:
        new_note = Subjects(subject_name = subject_name,
                            type = hw_type,
                            homework = content,
                            form = form,
                            group = group,
                            comment = comment,
                            editor = editor,
                            date = timestamp)
        self.session.add(new_note)
        await self.session.commit()
        return new_note

class SubjectService:
    def __init__(self,repo: SubjectRepository):
        self._repo = repo

    async def add_task(self, subject_name, form,
                       editor, comment,
                       hw_type, content,
                       timestamp: datetime.date = f'{str(datetime.time())[:5]} {datetime.date.today()}',
                       group = '0'):
        result = await self._repo.add_or_update_note(subject_name = subject_name,
                                               form=form,
                                               editor = editor,
                                               comment=comment,
                                               hw_type = hw_type,
                                               content= content,
                                               group = group,
                                               timestamp = timestamp)

        return result

    async def get_subject_note(self,subject_name, form, group,):
        result = await self._repo.get_subject_task(subject_name = subject_name,
                                                    form = form,
                                                    group = group)


        return result



