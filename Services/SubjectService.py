from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Infrastructure.Tables.Subjects import Subjects
from abc import ABC,abstractmethod
import datetime

class ISubjectRepository(ABC):
    @abstractmethod
    async def add_new_note(self,subject_name, form, editor, timestamp, comment, hw_type, content , group = '0') -> Subjects: ...

    @abstractmethod
    async def get_subject_task(self, subject_name, form, group) -> Subjects: ...

class SubjectRepository(ISubjectRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_subject_task(self,subject_name, form, group) -> Subjects:
        result = await  self.session.execute(select(Subjects).filter(Subjects.subject_name == subject_name and (Subjects.form == form and Subjects.group in (group,'0'))).limit(1))
        return result.scalar()

    async def add_new_note(self,subject_name, form, editor, timestamp, comment, hw_type, content , group = 0) -> Subjects:
        new_note = Subjects(subject_name = subject_name,
                            type = hw_type,
                            homework = content,
                            form = form,
                            group = group,
                            comment = comment,
                            date = f'{timestamp} @{editor}')
        self.session.add(new_note)
        await self.session.commit()
        return new_note

class SubjectService:
    def __init__(self,repo: SubjectRepository):
        self._repo = repo

    async def add_task(self,subject_name, form, editor, comment, hw_type, content , group = '0'):
        timestamp = str(datetime.date.today())
        result = await self._repo.add_new_note(subject_name = subject_name,
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
        return  result



