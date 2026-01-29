"""
Базовый класс для всех шаблонов кнопок
"""

from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup


class BaseKeyboardTemplate(ABC):
    """Базовый класс для всех шаблонов кнопок"""

    @abstractmethod
    def build(self, **context) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру из шаблона

        Args:
            **context: Контекстные переменные для подстановки в текст кнопок

        Returns:
            InlineKeyboardMarkup: Готовая клавиатура для aiogram
        """
        pass
