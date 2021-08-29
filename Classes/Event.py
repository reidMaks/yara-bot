from typing import TypeVar, Type, Generator, Optional
from db import DB, EventModel
from repository import EventManager

T = TypeVar('T', bound='Event')


class Event(EventModel):
    __session = DB().session

    @classmethod
    def find_event_by_id(cls: Type[T], event_id: int) -> Optional[T]:
        res = cls.__session.query().filter_by(id=event_id)
        if res:
            first = res.first()
            return first if isinstance(first, Event) else None
        else:
            return None

    @classmethod
    def find_events(cls, *args) -> Generator[None, T, None]:
        res = cls.__session.query(EventModel).filter(*args).order_by(EventModel.time.desc()).all()

        if not res:
            return None

        for i in res:
            yield i

    @classmethod
    def remove_event_by_id(cls: Type[T], event_id: int):
        res = cls.find_event_by_id(event_id)

        if res:
            res.remove()

    def is_long(self):
        """Событие имеет продолжительность во времени"""
        pass

    def save(self):
        self.__session.add(self)
        self.__session.commit()

    def remove(self):
        if self.id is not None:
            self.__session.filter_by(id=self.id) \
                .delete()

    def update(self, new_value: dict):

        for key, value in new_value.items():
            if key in vars(self).keys():
                self[key] = value
            else:
                raise AttributeError(f'Object don\'t have attribute "{key}"')

        self.save()

    def set_ib_session(self, session: DB.session) -> None:
        self.__session = session


class FlashEvent(Event):
    @property
    def is_long(self):
        return False
