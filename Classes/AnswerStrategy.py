from abc import ABC, abstractmethod


class Strategy(ABC):

    @property
    @abstractmethod
    def trigger(self):
        pass

    @abstractmethod
    def execute(self):
        pass
