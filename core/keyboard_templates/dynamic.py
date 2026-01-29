"""
Шаблон для динамических кнопок с функцией-билдером
"""

from typing import Callable
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base import BaseKeyboardTemplate


class DynamicTemplate(BaseKeyboardTemplate):
    """Шаблон для динамических кнопок с пользовательской логикой"""

    def __init__(self, buttons_builder: Callable):
        """
        Инициализация динамического шаблона

        Args:
            buttons_builder: Функция, которая принимает контекст и возвращает список кнопок
        """
        self.buttons_builder = buttons_builder

    def build(self, **context) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру с динамически генерируемыми кнопками

        Args:
            **context: Контекстные переменные для передачи в билдер

        Returns:
            InlineKeyboardMarkup: Динамически созданная клавиатура
        """
        # Получаем кнопки от функции-билдера
        buttons_config = self.buttons_builder(context)

        keyboard = []

        for button_config in buttons_config:
            # Подстановка значений из контекста
            text = button_config["text"].format(**context)
            callback_data = button_config.get("callback_data", "").format(**context)
            url = button_config.get("url")

            # Создание кнопки
            if url:
                button = InlineKeyboardButton(text=text, url=url)
            else:
                button = InlineKeyboardButton(text=text, callback_data=callback_data)

            # Определяем структуру рядов
            if button_config.get("row", "auto") == "separate":
                # Каждая кнопка в отдельном ряду
                keyboard.append([button])
            else:
                # Автоматическое распределение или указанный ряд
                row_index = button_config.get("row_index", len(keyboard) - 1 if keyboard else 0)
                if row_index >= len(keyboard):
                    keyboard.append([button])
                else:
                    keyboard[row_index].append(button)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
