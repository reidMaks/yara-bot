from abc import *
from db import DB, EventModel


class Event(ABC, EventModel):
    __session = DB().session

    @classmethod
    def find_event(cls, event_id: int):
        return cls.__session.query().filter_by(id=event_id).first()

    @property
    @abstractmethod
    def is_long(self):
        """Событие имеет продолжительность во времени"""
        pass

    def save(self):
        self.__session.add(self)
        self.__session.commit()

    def remove(self):
        if self.id is not None:
            self.__session.filter_by(id=self.id)\
                .delete()

    def update(self, new_value):

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
        pass


    def update(self):
        pass
