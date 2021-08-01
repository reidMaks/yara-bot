import re

from config import DB_URL, isProduction
import datetime
import enum
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

__all__ = ["Event", "User"]

engine = create_engine(DB_URL, echo=not isProduction(), pool_size=20, max_overflow=0)
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
    play = 'play'

    def __str__(self):
        reprs = {'eat': 'Ели',
                 'sleep': 'Спали',
                 'shit': 'Какали',
                 'walk': 'Гуляли',
                 'bath': 'Купались',
                 'play': 'Бодрствовали'
                 }
        return reprs[self.name]


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
        regex = r"^\s*$\n"
        r = f"""
            Событие [{self.id}]:
                Действие:       {self.type}
                Начало события: {format(self.time, '%d.%m %H:%M')}
                {'' if self.end_time is None else "Конец события:        " + format(self.end_time, '%d.%m %H:%M')}
                {'' if self.value == 0 else "Количество:        " + str(self.value) + " мл."}
                {'' if self.comment == "" else "Комментарий:    " + self.comment}
            """
        return re.sub(regex, "", r, 0, re.MULTILINE | re.IGNORECASE)

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
