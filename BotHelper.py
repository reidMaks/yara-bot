from telebot import types
import datetime

from Classes.Event import Event, EventModel
from db import EventType


class ButtonManager:

    @staticmethod
    def get_start_keyboard() -> types.ReplyKeyboardMarkup:
        eat_btn = types.KeyboardButton('🍼Еда')
        sleep_btn = types.KeyboardButton('😴 Сон')
        walk_btn = types.KeyboardButton('🚶 Прогулка')
        shit_btn = types.KeyboardButton('💩 О мой б-г, это случилось')
        bath_btn = types.KeyboardButton('🛁 Купание')
        stat_btn = types.KeyboardButton('📈 Статистика')

        markup = types.ReplyKeyboardMarkup(selective=True, resize_keyboard=True)

        markup.add(walk_btn, bath_btn, sleep_btn)
        markup.add(shit_btn, eat_btn)
        markup.add(stat_btn)

        return markup


def begin_of_current_day():
    return datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


def time_from_last(event_type: str) -> [str, None]:
    from datetime import timedelta, datetime
    for event in Event.find_events(EventModel.type == event_type):
        if event.end_time:
            delta = datetime.today() - max(event.time, event.end_time)
        else:
            delta = datetime.today() - event.time
        return timedelta(seconds=delta.seconds)
    else:
        return None


def last_eat_time_message() -> str:
    last = time_from_last('eat')

    if last is None:
        return "Время не известно"

    m = last.seconds / 60

    emoji = {
        m < 60: '🙂',
        60 <= m < 90: '🤔',
        90 <= m < 120: '😕',
        120 <= m < 180: '😡',
        180 <= m: '🤬'
    }[True]

    return f"{emoji} {last}"
