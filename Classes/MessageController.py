from TGbot import types as tt
import TGbot
from typing import Union, overload, TypedDict, Type, TypeVar
import Classes.AnswerStrategy


class Answer(TypedDict):
    text: str


class AnswerKeyboard(Answer):
    markup: Union[tt.ReplyKeyboardMarkup, tt.InlineKeyboardMarkup, None]


C = TypeVar('C')


class MessageController:
    message: Union[tt.Message, tt.CallbackQuery]
    strategy: Type[C]
    answer: Union[Answer, AnswerKeyboard]

    def __init__(self, message):
        self.message = message

    def set_strategy(self, strategy: Type[C]):
        self.strategy = strategy(self.message, self)

    def send_answer(self):
        self.strategy.execute()
        if type(self.message) is tt.Message:
            self.send_msg_answer(self.message, self.answer)
        else:
            self.send_call_answer(self.message, self.answer)

    @staticmethod
    def send_msg_answer(message: tt.Message, answer: Union[Answer, AnswerKeyboard]) -> None:
        if answer.get("markup") is None:
            answer.setdefault("markup")

        TGbot.bot.reply_to(message, answer["text"], reply_markup=answer["markup"])

    @staticmethod
    def send_call_answer(message: tt.CallbackQuery, answer: Union[Answer, AnswerKeyboard]) -> None:
        TGbot.bot.answer_callback_query(message.id, text=answer["text"])
