from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base


database_engine = create_engine('sqlite:///main.db')
Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer,primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    form = Column(String(10))
    group = Column(String(3))
    privileges = Column(String)


Base.metadata.create_all(database_engine)
