from abc import ABC, abstractmethod
from aiogram import Router

class BotRouter(ABC):

    @property
    @abstractmethod
    def router(self) -> Router:
        """Возвращает aiogram.Router с зарегистрированными хендлерами"""
        pass
