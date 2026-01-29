"""
Шаблон для кнопок в сетке (несколько кнопок в ряду)
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base import BaseKeyboardTemplate


class GridTemplate(BaseKeyboardTemplate):
    """Шаблон для кнопок, расположенных в сетке"""

    def __init__(self, buttons: list, columns: int = 2):
        """
        Инициализация шаблона сетки

        Args:
            buttons: Список словарей с настройками кнопок
            columns: Количество кнопок в одном ряду (по умолчанию 2)
        """
        self.buttons = buttons
        self.columns = columns

    def build(self, **context) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру в виде сетки

        Args:
            **context: Контекстные переменные для подстановки

        Returns:
            InlineKeyboardMarkup: Готовая клавиатура в виде сетки
        """
        keyboard = []
        current_row = []

        for i, button_config in enumerate(self.buttons):
            # Подстановка значений из контекста
            text = button_config["text"].format(**context)
            callback_data = button_config.get("callback_data", "").format(**context)
            url = button_config.get("url")

            # Создание кнопки
            if url:
                button = InlineKeyboardButton(text=text, url=url)
            else:
                button = InlineKeyboardButton(text=text, callback_data=callback_data)

            current_row.append(button)

            # Если достигли нужного количества кнопок в ряду или это последняя кнопка
            if len(current_row) == self.columns or i == len(self.buttons) - 1:
                keyboard.append(current_row)
                current_row = []

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
