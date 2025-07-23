from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

class DataBase:
    def __init__(self,db_url = 'sqlite+aiosqlite:///main.db'):
        self.engine = create_async_engine(db_url, echo = True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False,autoflush=False)

    @asynccontextmanager
    async def session_make(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()