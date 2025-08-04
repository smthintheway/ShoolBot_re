from sqlalchemy import create_engine,Column,Integer,String,Enum
from sqlalchemy.orm import declarative_base
import enum
import json

database_engine = create_engine('sqlite:///main.db')
Base = declarative_base()


class Weekday(enum.Enum):
    MONDAY = "Понедельник"
    TUESDAY = "Вторник"
    WEDNESDAY = "Среда"
    THURSDAY = "Четверг"
    FRIDAY = "Пятница"
    SATURDAY = "Суббота" 



class Schedule(Base):
    __tablename__ = 'Schedule'

    id = Column(Integer,primary_key=True)
    form = Column(String)
    monday_schedule = Column(String)
    tuesday_schedule = Column(String)
    wednesday_schedule = Column(String)
    friday_schedule = Column(String)
    saturday_schedule = Column(String)


Base.metadata.create_all(database_engine)
