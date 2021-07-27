from db import Event, Session, EventType
from typing import Union
from datetime import datetime, timedelta


def get_session() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()


def statistic(callback_data: str) -> Union[str, int, bool, timedelta, None]:
    section, question, time, event_type = callback_data.split(',')
    if section != 'statistic':
        return None

    if event_type not in EventType.__members__:
        return None

    if time == 'today':
        time = datetime.today()
    elif time == 'yesterday':
        time = datetime.today() - timedelta(days=1)
    else:
        time = datetime(1, 1, 1)

    session = next(get_session())
    result = session.query(Event) \
        .filter(Event.type == event_type, Event.time <= time) \
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

        if question == 'how-long-ago':
            return datetime.today() - max(record.time, record.end_time)

    if question == 'how-many':
        return sum_count

    if question == 'how-much':
        return sum_value


class EventManager:
    session = next(get_session())

    def save_event(self, event: Event):
        self.session.add(event)
        self.session.commit()

        return self.session.query(Event).filter_by(time=event.time).first()

    def update_event(self, event_id: int, new_value: dict):
        event = self.query().filter_by(id=event_id).first()

        for key, value in new_value.items():
            event[key] = value

        self.save_event(event)

    def query(self):
        return self.session.query(Event)
