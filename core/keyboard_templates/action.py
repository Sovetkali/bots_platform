"""
Шаблон для кнопок действий (подтверждение/отмена)
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base import BaseKeyboardTemplate


class ActionTemplate(BaseKeyboardTemplate):
    """Шаблон для кнопок действий с подтверждением"""

    def __init__(self, confirm_text: str = "✅ Да", cancel_text: str = "❌ Нет",
                 confirm_data: str = "confirm", cancel_data: str = "cancel"):
        """
        Инициализация шаблона действий

        Args:
            confirm_text: Текст кнопки подтверждения
            cancel_text: Текст кнопки отмены
            confirm_data: callback_data для подтверждения
            cancel_data: callback_data для отмены
        """
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.confirm_data = confirm_data
        self.cancel_data = cancel_data

    def build(self, **context) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру с кнопками подтверждения и отмены

        Args:
            **context: Контекстные переменные для подстановки

        Returns:
            InlineKeyboardMarkup: Клавиатура с действиями
        """
        # Подстановка значений из контекста
        confirm_text = self.confirm_text.format(**context)
        cancel_text = self.cancel_text.format(**context)
        confirm_data = self.confirm_data.format(**context)
        cancel_data = self.cancel_data.format(**context)

        # Создаем кнопки в одном ряду
        keyboard = [
            [
                InlineKeyboardButton(text=confirm_text, callback_data=confirm_data),
                InlineKeyboardButton(text=cancel_text, callback_data=cancel_data)
            ]
        ]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
