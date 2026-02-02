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
