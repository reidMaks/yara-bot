from abc import ABC, abstractmethod
from telebot import types as tt
from typing import Union
from Classes.MessageController import MessageController
from config import OWNERS
from BotHelper import ButtonManager


class Strategy(ABC):
    trigger: Union[tt.Message, tt.CallbackQuery]
    owner: MessageController

    @abstractmethod
    def execute(self):
        pass

    def __init__(self, message: Union[tt.Message, tt.CallbackQuery],
                 owner: MessageController):
        self.trigger = message
        self.owner = owner

    def check_permission(self) -> bool:
        return OWNERS.find(str(self.trigger.from_user.id)) >= 0

    def set_permission_denied_answer(self):
        self.owner.answer = {"text": f"""{self.trigger.from_user.username}, 
                                    access denied. contact the administrator @kms_live"""}

class StartCommandStrategy(Strategy):
    def execute(self):
        if not self.check_permission():
            self.set_permission_denied_answer()
            return

        keyboard = ButtonManager.get_start_keyboard()

        self.owner.answer = {"text": f"""{self.trigger.from_user.username}, 
                                            access granted!""",
                             "markup": keyboard}
