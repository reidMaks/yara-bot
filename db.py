from config import DB_URL
import datetime
import enum
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

__all__ = ["Event", "User"]

engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class EventType(enum.Enum):
    eat = 'eat'
    sleep = 'sleep'
    shit = 'shit'
    walk = 'walk'
    bath = 'bath'


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(EventType))
    time = Column(DateTime)
    end_time = Column(DateTime)
    value = Column(Integer)
    comment = Column(String)

    def __init__(self, type, time=None, value=0, comment=''):
        self.type = type
        if time is None:
            self.time = datetime.datetime.now()
        else:
            self.time = time
        self.value = value
        self.comment = comment

    def __repr__(self):
        return "Событие (%s, %s, %s, %s)" % (format(self.time, '%d.%m %H:%M'), self.type, self.value, self.comment)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    name = Column(String)
    is_master = Column(Boolean)

    def __repr__(self):
        return "Пользователь (%s, %s)" % (self.tg_id, self.name)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
