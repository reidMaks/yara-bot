from abc import ABC, abstractmethod
from telebot import types as tt
from telebot import TeleBot
from typing import Union, Callable, Type, TypedDict

from config import OWNERS
from BotHelper import ButtonManager, begin_of_current_day


class Answer(TypedDict):
    text: str


class AnswerKeyboard(Answer):
    markup: Union[tt.ReplyKeyboardMarkup, tt.InlineKeyboardMarkup, tt.ReplyKeyboardRemove, None]


class MessageController:

    def __init__(self, message: Union[tt.Message, tt.CallbackQuery], bot: TeleBot):
        self.message: Union[tt.Message, tt.CallbackQuery] = message
        self._answer: Union[Answer, AnswerKeyboard]
        self.bot: TeleBot = bot
        self.strategy: Type[Strategy]

    def set_strategy(self, strategy):
        self.strategy = strategy(self)

    def set_answer(self, answer: Union[Answer, AnswerKeyboard]):
        self._answer = answer

    def send_answer(self):
        self.strategy.execute()
        if type(self.message) is tt.Message:
            self.send_msg_answer(self.message, self.answer, self.bot)
        else:
            self.send_call_answer(self.message, self.answer, self.bot)

    @staticmethod
    def send_msg_answer(message: tt.Message, answer: AnswerKeyboard, bot: TeleBot) -> None:

        if answer.get("markup") is None:
            answer.setdefault("markup", None)

        bot.reply_to(message, answer["text"], reply_markup=answer["markup"])

    @staticmethod
    def send_call_answer(message: tt.CallbackQuery, answer: Union[Answer, AnswerKeyboard],
                         bot: TeleBot) -> None:
        bot.answer_callback_query(message.id, text=answer["text"])


def check_permission(self, method: Callable):
    if not isinstance(self, Strategy):
        raise Exception('Декоратор предназначен только для методов Strategy')

    def wrapper(*args, **kwargs):
        if not OWNERS.find(str(self.trigger.from_user.id)) >= 0:
            self.set_permission_denied_answer()
            return

        return method(self, *args, **kwargs)

    return wrapper


class Strategy(ABC):

    def __init__(self, owner: MessageController):
        self.trigger: Union[tt.Message, tt.CallbackQuery] = owner.message
        self.owner: Type[MessageController] = owner

    def __getattribute__(self, name):
        if name == "execute":  # Реализация декоратора для имплементируемых методов execute
            func = getattr(type(self), "execute")
            return check_permission(self, func)
        return object.__getattribute__(self, name)

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def set_permission_denied_answer(self):
        ans = {"text": f"""{self.trigger.from_user.username} <{self.trigger.from_user.id}>, 
                                    access denied. contact the administrator @kms_live""",
               "markup": tt.ReplyKeyboardRemove()}

        self.owner.set_answer(ans)


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
        ans = {"text": text, "markup": None}

        self.owner.set_answer(ans)


class EventsCommandStrategy(Strategy):
    def execute(self):
        from Classes.Event import EventModel, Event
        b_date = begin_of_current_day()
        result = Event.find_events(Event.time >= b_date) \
            .order_by(Event.time.desc()).all()

        answer = [str(i) for i in result]

        if len(answer) == 0:
            answer = ["Событий нет"]

        ans = {"text": answer, "markup": None}
        self.owner.set_answer(ans)
