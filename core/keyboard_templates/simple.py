"""
Шаблон для простых кнопок в один ряд
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base import BaseKeyboardTemplate


class SimpleTemplate(BaseKeyboardTemplate):
    """Шаблон для простых кнопок в один ряд"""

    def __init__(self, buttons: list):
        """
        Инициализация шаблона

        Args:
            buttons: Список словарей с настройками кнопок
                Пример: [
                    {"text": "Кнопка 1", "callback_data": "action1"},
                    {"text": "Кнопка 2", "callback_data": "action2"}
                ]
        """
        self.buttons = buttons

    def build(self, **context) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру из шаблона

        Args:
            **context: Контекстные переменные для подстановки в текст кнопок

        Returns:
            InlineKeyboardMarkup: Готовая клавиатура
        """
        keyboard = []

        for button_config in self.buttons:
            # Подстановка значений из контекста в текст и callback_data
            text = button_config["text"].format(**context)
            callback_data = button_config.get("callback_data", "").format(**context)
            url = button_config.get("url")

            # Создание кнопки
            if url:
                button = InlineKeyboardButton(text=text, url=url)
            else:
                button = InlineKeyboardButton(text=text, callback_data=callback_data)

            # Каждая кнопка в отдельном ряду
            keyboard.append([button])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
