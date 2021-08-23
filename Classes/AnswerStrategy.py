from abc import ABC, abstractmethod
from telebot import types as tt
from typing import Union, Callable, Protocol
from Classes.MessageController import MessageController
from config import OWNERS
from BotHelper import ButtonManager, begin_of_current_day


def check_permission(self, method: Callable):
    if not isinstance(self, Strategy):
        raise Exception('Декоратор предназначен только для методов Strategy')

    def wrapper(*args, **kwargs):
        if not OWNERS.find(str(self.trigger.from_user.id)) >= 0:
            self.set_permission_denied_answer()
            return

        return method(self, *args, **kwargs)

    return wrapper


class Executable(Protocol):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class Strategy(ABC, Executable):
    trigger: Union[tt.Message, tt.CallbackQuery]
    owner: MessageController

    def __init__(self, message: Union[tt.Message, tt.CallbackQuery],
                 owner: MessageController):
        self.trigger = message
        self.owner = owner

    def __getattribute__(self, name):
        if name == "execute":
            func = getattr(type(self), "execute")
            return check_permission(self, func)
        return object.__getattribute__(self, name)

    def set_permission_denied_answer(self):
        self.owner.answer = {"text": f"""{self.trigger.from_user.username} <{self.trigger.from_user.id}>, 
                                    access denied. contact the administrator @kms_live""",
                             "markup": tt.ReplyKeyboardRemove()}


class StartCommandStrategy(Strategy):
    def execute(self):
        keyboard = ButtonManager.get_start_keyboard()

        self.owner.answer = {"text": f"""{self.trigger.from_user.username}, 
                                            access granted!""",
                             "markup": keyboard}


class HelpCommandStrategy(Strategy):
    def execute(self):
        text = """
        Бот принимает команды из ручного ввода
        Например: <еда 17:00 120>  создаст событие
            ожидается следующий ввод:
            :первое слово - тип актвности из списка(еда|прогулка|купание|покакали|сон)
            :далее через пробел время начала события. Если время больше текущего времени сервера
                будет предложено создать событие вчерашней датой
            :далее ожидается значение количества целым числом, если у события нет количествоенного 
                измерения (например купание) следует передать 0
            """
        self.owner.answer = {"text": text, "markup": None}


class EventsCommandStrategy(Strategy):
    def execute(self):
        from Classes.Event import EventModel, Event
        b_date = begin_of_current_day()
        result = Event.find_events(Event.time >= b_date) \
            .order_by(Event.time.desc()).all()

        answer = [str(i) for i in result]

        if len(answer) == 0:
            answer = ["Событий нет"]

        self.owner.answer = {"text": answer,
                             "markup": None}
