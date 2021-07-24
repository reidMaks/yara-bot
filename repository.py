from db import Event, Session


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


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
