import os
import datetime
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

pg_user = os.environ.get('PG_USER', '')
pg_pwd = os.environ.get('PG_PWD', '')
pg_srv = os.environ.get('PG_SRV', '')

engine = create_engine(f"postgresql://{pg_user}:{pg_pwd}@{pg_srv}/yara-bd", echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    type = Column(Enum("eat", "sleep", "shit", "walk", name="event_type", create_type=False))
    time = Column(DateTime)
    value = Column(Integer)
    comment = Column(String)

    def __init__(self, type, time=datetime.datetime.now(), value=0, comment=''):
        self.type = type
        self.time = time
        self.value = value
        self.comment = comment

    def __repr__(self):
        return "<Event('%s','%s', '%s')>" % (self.type, self.value, self.comment)


Base.metadata.create_all(engine)
