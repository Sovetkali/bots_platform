#!/usr/bin/env python3
"""
Тест для проверки функциональности регистрации пользователей и работы с ботами
"""

import asyncio
import sys
import os

# Добавляем корневую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import db
from services.user_service import UserService
from core.models.user import User as UserModel


async def test_user_registration():
    """Тест регистрации пользователя и связи с ботом"""
    print("🧪 Тестирование регистрации пользователя и работы с ботами...")

    async with db.session() as session:
        user_service = UserService(session)

        # Тест 1: Регистрация нового пользователя
        print("\n1. Тест регистрации нового пользователя:")
        test_user = UserModel(
            tg_id=123456789,
            name='Test User',
            lang='ru'
        )

        try:
            db_user, bot, user_bot = await user_service.register_user_with_bot(
                test_user,
                bot_code='test_bot',
                bot_name='Test Bot'
            )

            print(f'✓ Пользователь зарегистрирован: ID={db_user.id}, Telegram ID={db_user.telegram_id}')
            print(f'✓ Бот создан: ID={bot.id}, Code={bot.code}, Name={bot.name}')
            print(f'✓ Связь создана: UserBot ID={user_bot.id}, First Used At={user_bot.first_used_at}')
        except Exception as e:
            print(f'✗ Ошибка при регистрации: {e}')
            return False

        # Тест 2: Получение пользователя по telegram_id
        print("\n2. Тест получения пользователя по telegram_id:")
        try:
            found_user = await user_service.get_user_by_telegram_id(123456789)
            if found_user and found_user.name == 'Test User':
                print(f'✓ Пользователь найден: {found_user.name}')
            else:
                print('✗ Пользователь не найден или данные не совпадают')
                return False
        except Exception as e:
            print(f'✗ Ошибка при поиске пользователя: {e}')
            return False

        # Тест 3: Получение списка ботов пользователя
        print("\n3. Тест получения списка ботов пользователя:")
        try:
            user_bots = await user_service.get_user_bots(123456789)
            if user_bots and len(user_bots) > 0:
                print(f'✓ Боты пользователя: {[bot.name for bot in user_bots]}')
            else:
                print('✗ Боты пользователя не найдены')
                return False
        except Exception as e:
            print(f'✗ Ошибка при получении ботов: {e}')
            return False

        # Тест 4: Регистрация существующего пользователя с новым ботом
        print("\n4. Тест регистрации существующего пользователя с новым ботом:")
        try:
            db_user2, bot2, user_bot2 = await user_service.register_user_with_bot(
                test_user,
                bot_code='test_bot_2',
                bot_name='Test Bot 2'
            )

            print(f'✓ Пользователь обновлен: ID={db_user2.id}')
            print(f'✓ Новый бот создан: ID={bot2.id}, Code={bot2.code}')
            print(f'✓ Новая связь создана: UserBot ID={user_bot2.id}')

            # Проверяем, что у пользователя теперь 2 бота
            user_bots_after = await user_service.get_user_bots(123456789)
            if len(user_bots_after) == 2:
                print(f'✓ У пользователя {len(user_bots_after)} ботов: {[bot.name for bot in user_bots_after]}')
            else:
                print(f'✗ Ожидалось 2 бота, получено {len(user_bots_after)}')
                return False

        except Exception as e:
            print(f'✗ Ошибка при регистрации с новым ботом: {e}')
            return False

        # Тест 5: Попытка создать дублирующую связь
        print("\n5. Тест предотвращения дублирующих связей:")
        try:
            db_user3, bot3, user_bot3 = await user_service.register_user_with_bot(
                test_user,
                bot_code='test_bot',  # Тот же бот
                bot_name='Test Bot'   # Тот же бот
            )

            # Должна вернуться существующая связь
            if user_bot3.id == user_bot.id:
                print('✓ Дублирующая связь предотвращена, возвращена существующая')
            else:
                print('✗ Создана новая связь вместо использования существующей')
                return False

        except Exception as e:
            print(f'✗ Ошибка при проверке дублирующей связи: {e}')
            return False

    print("\n🎉 Все тесты пройдены успешно!")
    return True


async def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("Тестирование системы регистрации пользователей и ботов")
    print("=" * 60)

    success = await test_user_registration()

    if success:
        print("\n✅ Система работает корректно!")
        return 0
    else:
        print("\n❌ Обнаружены проблемы в системе!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
