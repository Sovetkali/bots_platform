# Документация Mommy Platform

## Обзор

Mommy Platform - это модульная платформа для создания и управления Telegram ботами на основе aiogram. Платформа предоставляет четкую архитектуру с разделением ответственности между компонентами.

## Содержание

### Основная документация
- [Создание нового бота](создание-бота.md) - Полное руководство по созданию бота с нуля

### Архитектура
- **Модульная структура**: Каждый бот - отдельный модуль с четкими границами
- **Factory Pattern**: Регистрация ботов через фабричные функции
- **Simple Container**: Упрощенный контейнер для создания компонентов бота
- **Registry Pattern**: Централизованное управление ботами через реестр
- **Database Layer**: Асинхронная работа с PostgreSQL через SQLAlchemy
- **Repository Pattern**: Изоляция логики доступа к данным

### Ключевые компоненты
- **BotRegistry** - Центральный реестр для управления ботами
- **BotContainer** - Упрощенный контейнер для создания компонентов бота
- **BotClient** - Абстракция клиента бота (aiogram-based)
- **BotRouter** - Маршрутизация команд и сообщений
- **BotService** - Бизнес-логика бота
- **Database** - Конфигурация и управление подключением к БД
- **Models** - Модели данных SQLAlchemy
- **Repositories** - Паттерн репозитория для работы с данными
- **Filters** - Фильтры для обработки сообщений
- **Middlewares** - Middleware для обработки запросов

## Быстрый старт

1. **Настройте базу данных**: Установите PostgreSQL и создайте БД
2. **Настройте конфигурацию**: Добавьте параметры БД в `.env` и `config.py`
3. **Примените миграции**: `alembic upgrade head`
4. **Изучите архитектуру**: Прочитайте [создание-бота.md](создание-бота.md)
5. **Создайте структуру**: Следуйте пошаговой инструкции
6. **Зарегистрируйте бота**: Добавьте фабричную функцию в `__init__.py`
7. **Запустите платформу**: `python main.py`

## Примеры

Изучите существующий бот в папке [`bots/srv_servicebot/`](../bots/srv_servicebot/) для понимания практической реализации.

## Работа с базой данных

### Модели данных
Модели SQLAlchemy находятся в [`core/models/db/`](../core/models/db/). Пример модели пользователя:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    lang = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### Репозитории
Репозитории для работы с данными в [`core/repositories/`](../core/repositories/):
```python
class UserRepository:
    async def create_user(self, *, user_id: int, name: str, lang: str) -> User:
        user = User(id=user_id, name=name, lang=lang)
        self.session.add(user)
        await self.session.flush()
        return user
```

### Миграции
Используйте Alembic для управления схемой базы данных:
```bash
# Создание миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head
```

## Фильтры и Middleware

### Фильтры
Фильтры позволяют гибко настраивать обработку сообщений. Пример фильтра для приватных чатов:

```python
from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsPrivateChat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"

# Применение фильтра
self._router.message.register(self.start, Command("start"), IsPrivateChat())
```

### Middleware
Middleware позволяют обрабатывать запросы до их достижения обработчиков. Пример middleware для исключения ботов:

```python
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Any, Awaitable
from utils.telegram import get_user_from_update

class IsBotMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict
    ):
        user = get_user_from_update(event)

        if not user:
            return await handler(event, data)

        if user.is_bot:
            return

        return await handler(event, data)

# Применение middleware
self.dp.update.middleware(IsBotMiddleware())
```

### Утилиты для работы с Telegram
Для извлечения пользователя из обновления используется утилитарная функция:

```python
from aiogram.types import Update, User

def get_user_from_update(update: Update) -> User | None:
    if update.message:
        return update.message.from_user
    if update.callback_query:
        return update.callback_query.from_user
    if update.inline_query:
        return update.inline_query.from_user
    return None
```

## Поддержка

При возникновении проблем:
1. Проверьте раздел "Возможные проблемы и их решения" в основной документации
2. Убедитесь в правильности конфигурации
3. Проверьте логи приложения

---
*Документация обновлена: 2026-02-02*
*Добавлена информация о фильтрах, middleware и утилитах для работы с Telegram*
