from aiogram import BaseMiddleware
from services.user_service import UserService

class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        session = data["db_session"]
        data["user_service"] = UserService(session)

        return await handler(event, data)
