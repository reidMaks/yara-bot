from db import Event, Session, EventType
from typing import Union, Optional
from datetime import datetime, timedelta


def get_session() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()


event_type_map = {
    "еда": 'eat',
    "сон": 'sleep',
    "покакали": 'shit',
    "прогулка": 'walk',
    "купание": 'bath',
    "бодрствование": 'play'
}


def statistic(callback_data: str) -> Union[str, int, bool, timedelta, None]:
    section, question, time, event_type = callback_data.split(',')
    if section != 'statistic':
        return None

    if event_type not in EventType.__members__:
        return None

    today = datetime.today()
    if time == 'today':
        # todo: Вынести в аналог началоДня() или найти готовый
        time = today - timedelta(hours=today.hour, minutes=today.minute, seconds=today.second)
    elif time == 'yesterday':

        time = today - timedelta(days=1, hours=today.hour, minutes=today.minute, seconds=today.second)
    else:
        time = datetime(1, 1, 1)

    session = next(get_session())
    result = session.query(Event) \
        .filter(Event.type == event_type, Event.time >= time) \
        .order_by(Event.time.desc())

    if result.count() == 0:
        return None

    sum_value = 0
    sum_count = 0
    for record in result:
        sum_value += record.value
        sum_count += 1

        if question == 'have':
            return True
        elif question == 'how-long-ago':
            if record.end_time is not None:
                delta = datetime.today() - max(record.time, record.end_time)
            else:
                delta = datetime.today() - record.time
            return str(timedelta(seconds=delta.seconds))

    if question == 'how-many':
        return sum_count

    if question == 'how-much':
        return sum_value


class EventManager:
    session = next(get_session())

    def create_event(self, event_type: Union[str, EventType], time: Union[datetime, str], value: Union[int, str]) \
            -> Optional[Event]:

        if type(event_type) is str and event_type_map[event_type.lower()] in EventType.__members__:
            event_type = EventType[event_type_map[event_type.lower()]]

        if type(event_type) is not EventType:
            raise Exception('Не верный параметр event_type')

        if type(time) is str:
            time = datetime.strptime(time, "%H:%M")
            now = datetime.now()
            time = time.replace(now.year, now.month, now.day)

        if type(time) is not datetime:
            raise Exception('Не верный параметр time')

        value = int(value)

        event = Event(type=event_type, time=time, value=value)

        return self.save_event(event)

    def save_event(self, event: Event):
        self.session.add(event)
        self.session.commit()

        return self.session.query(Event).filter_by(time=event.time).first()

    def update_event(self, event_id: int, new_value: dict):
        event = self.query().filter_by(id=event_id).first()

        for key, value in new_value.items():
            event[key] = value

        return self.save_event(event)

    def remove_event(self, event_id: int):
        self.query().filter_by(id=event_id).delete()
        self.session.commit()

    def query(self):
        return self.session.query(Event)
