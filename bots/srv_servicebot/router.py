from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from core.base.router import BotRouter

class ServiceBotRouter(BotRouter):
    def __init__(self):
        self._router = Router()
        self._router.message.register(self.start, Command("start"))

    @property
    def router(self) -> Router:
        return self._router

    async def start(self, message: Message):
        await message.answer("Hello! This is ServiceBot at your service.")
