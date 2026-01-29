"""
Шаблон для многоуровневых меню с кнопкой "Назад"
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base import BaseKeyboardTemplate


class MenuTemplate(BaseKeyboardTemplate):
    """Шаблон для меню с заголовком и кнопкой возврата"""

    def __init__(self, items: list, title: str = None, back_button: dict = None):
        """
        Инициализация шаблона меню

        Args:
            items: Список пунктов меню (словари с text и callback_data)
            title: Заголовок меню (опционально)
            back_button: Конфигурация кнопки "Назад" (опционально)
        """
        self.items = items
        self.title = title
        self.back_button = back_button

    def build(self, **context) -> InlineKeyboardMarkup:
        """
        Создает меню с возможными заголовком и кнопкой возврата

        Args:
            **context: Контекстные переменные для подстановки

        Returns:
            InlineKeyboardMarkup: Готовое меню
        """
        keyboard = []

        # Добавляем заголовок, если указан
        if self.title:
            title_text = self.title.format(**context)
            keyboard.append([InlineKeyboardButton(text=title_text, callback_data="menu_title")])

        # Добавляем пункты меню
        for item in self.items:
            text = item["text"].format(**context)
            callback_data = item.get("callback_data", "").format(**context)
            url = item.get("url")

            if url:
                button = InlineKeyboardButton(text=text, url=url)
            else:
                button = InlineKeyboardButton(text=text, callback_data=callback_data)

            keyboard.append([button])

        # Добавляем кнопку "Назад", если указана
        if self.back_button:
            back_text = self.back_button.get("text", "← Назад").format(**context)
            back_data = self.back_button.get("callback_data", "back").format(**context)
            keyboard.append([InlineKeyboardButton(text=back_text, callback_data=back_data)])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
