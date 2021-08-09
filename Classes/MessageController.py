from bot import types as tt
from bot import BOT
import typing
from AnswerStrategy import Strategy


class MessageController:
    message: tt.Message
    strategy: Strategy
    answer: str

    @typing.overload
    def __init__(self, message: tt.Message):
        self.message = message

    def __init__(self):
        raise NotImplementedError

    def answer(self):

