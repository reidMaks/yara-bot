import telebot
from telebot import types as tt
from typing import Union, TypedDict, Protocol, TypeVar, Type

from Classes.AnswerStrategy import Executable


class Answer(TypedDict):
    text: str


class AnswerKeyboard(Answer):
    markup: Union[tt.ReplyKeyboardMarkup, tt.InlineKeyboardMarkup, tt.ReplyKeyboardRemove, None]


strategy_type = TypeVar('strategy_type', bound='Executable')


class MessageController:
    message: Union[tt.Message, tt.CallbackQuery]
    strategy: strategy_type
    answer: Union[Answer, AnswerKeyboard]
    bot: telebot.TeleBot

    def __init__(self, message: Union[tt.Message, tt.CallbackQuery], bot: telebot.TeleBot):
        self.message = message
        self.bot = bot

    def set_strategy(self, strategy: strategy_type):
        self.strategy = strategy(self.message, self)

    def send_answer(self):
        self.strategy.execute()
        if type(self.message) is tt.Message:
            self.send_msg_answer(self.message, self.answer, self.bot)
        else:
            self.send_call_answer(self.message, self.answer, self.bot)

    @staticmethod
    def send_msg_answer(message: tt.Message, answer: AnswerKeyboard, bot: telebot.TeleBot) -> None:

        if answer.get("markup") is None:
            answer.setdefault("markup", None)

        bot.reply_to(message, answer["text"], reply_markup=answer["markup"])

    @staticmethod
    def send_call_answer(message: tt.CallbackQuery, answer: Union[Answer, AnswerKeyboard],
                         bot: telebot.TeleBot) -> None:
        bot.answer_callback_query(message.id, text=answer["text"])
