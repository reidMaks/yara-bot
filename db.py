from config import PG_PWD, PG_SRV, PG_USER
import datetime
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

engine = create_engine(f"postgresql://{PG_USER}:{PG_PWD}@{PG_SRV}/yara-bd", echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    type = Column(Enum("eat", "sleep", "shit", "walk", name="event_type", create_type=False))
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


Base.metadata.create_all(engine)

