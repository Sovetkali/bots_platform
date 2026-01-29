#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации работы системы шаблонов кнопок
"""

import sys
import os

# Добавляем корневую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.keyboard_templates import SimpleTemplate, GridTemplate, MenuTemplate, ActionTemplate

def test_simple_template():
    """Тестирование SimpleTemplate"""
    print("=== Тест SimpleTemplate ===")

    template = SimpleTemplate([
        {"text": "Кнопка 1", "callback_data": "btn1"},
        {"text": "Кнопка 2", "callback_data": "btn2"},
        {"text": "Кнопка с URL", "url": "https://example.com"}
    ])

    keyboard = template.build()
    print(f"Количество рядов: {len(keyboard.inline_keyboard)}")

    for i, row in enumerate(keyboard.inline_keyboard):
        print(f"Ряд {i+1}: {[btn.text for btn in row]}")

    print()

def test_grid_template():
    """Тестирование GridTemplate"""
    print("=== Тест GridTemplate ===")

    template = GridTemplate(
        columns=2,
        buttons=[
            {"text": "1", "callback_data": "1"},
            {"text": "2", "callback_data": "2"},
            {"text": "3", "callback_data": "3"},
            {"text": "4", "callback_data": "4"},
            {"text": "5", "callback_data": "5"}
        ]
    )

    keyboard = template.build()
    print(f"Количество рядов: {len(keyboard.inline_keyboard)}")

    for i, row in enumerate(keyboard.inline_keyboard):
        print(f"Ряд {i+1}: {[btn.text for btn in row]}")

    print()

def test_menu_template():
    """Тестирование MenuTemplate"""
    print("=== Тест MenuTemplate ===")

    template = MenuTemplate(
        title="Главное меню",
        items=[
            {"text": "Профиль", "callback_data": "profile"},
            {"text": "Настройки", "callback_data": "settings"},
            {"text": "Помощь", "callback_data": "help"}
        ],
        back_button={"text": "← Назад", "callback_data": "back"}
    )

    keyboard = template.build()
    print(f"Количество рядов: {len(keyboard.inline_keyboard)}")

    for i, row in enumerate(keyboard.inline_keyboard):
        print(f"Ряд {i+1}: {[btn.text for btn in row]}")

    print()

def test_action_template():
    """Тестирование ActionTemplate"""
    print("=== Тест ActionTemplate ===")

    template = ActionTemplate(
        confirm_text="✅ Да",
        cancel_text="❌ Нет",
        confirm_data="confirm",
        cancel_data="cancel"
    )

    keyboard = template.build()
    print(f"Количество рядов: {len(keyboard.inline_keyboard)}")

    for i, row in enumerate(keyboard.inline_keyboard):
        print(f"Ряд {i+1}: {[btn.text for btn in row]}")

    print()

def test_dynamic_context():
    """Тестирование подстановки контекста"""
    print("=== Тест подстановки контекста ===")

    template = SimpleTemplate([
        {"text": "Привет, {user_name}!", "callback_data": "greet_{user_id}"},
        {"text": "Баланс: {balance} руб.", "callback_data": "balance"}
    ])

    keyboard = template.build(user_name="Иван", user_id=123, balance=1000)

    for i, row in enumerate(keyboard.inline_keyboard):
        for btn in row:
            print(f"Кнопка: {btn.text} -> {btn.callback_data}")

    print()

if __name__ == "__main__":
    print("Демонстрация системы шаблонов кнопок\n")

    test_simple_template()
    test_grid_template()
    test_menu_template()
    test_action_template()
    test_dynamic_context()

    print("✅ Все тесты завершены успешно!")
