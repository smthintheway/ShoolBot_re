from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base


database_engine = create_engine('sqlite:///main.db')
Base = declarative_base()

class Schedule(Base):
    __tablename__ = 'Schedule'

    id = Column(Integer,primary_key=True)
    type = Column(String)
    date = Column(String)
    editor = Column(String)
    subject_name = Column(String)
    form = Column(String)
    group = Column(String(4))
    homework = Column(String)
    comment = Column(String)


Base.metadata.create_all(database_engine)
