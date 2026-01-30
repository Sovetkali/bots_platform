import asyncio
import contextlib
from aiogram import Bot, Dispatcher
from core.base.client import BotClient
from core.models.bot_mode import BotMode
from core.models.client_config import BotClientConfig
from utils.logger import logger

class AiogramBotClient(BotClient):
    def __init__(self, *, name: str, config: BotClientConfig):
        self.name = name
        self.config = config
        self.bot = Bot(token=config.token)
        self.dp = Dispatcher()

    async def start(self) -> None:
        if self.config.mode == BotMode.POLLING:
            logger.info(f"Starting bot '{self.name}' in POLLING mode.")
            await self.dp.start_polling(self.bot)
        elif self.config.mode == BotMode.WEBHOOK:
            await self.bot.set_webhook(self.config.webhook_url)

    async def stop(self) -> None:
        logger.info(f"Stopping bot '{self.name}'.")

        if self.config.mode == BotMode.WEBHOOK:
            await self.bot.delete_webhook(drop_pending_updates=False)
        elif self.config.mode == BotMode.POLLING:
            #TODO никогда не попадаем сюда. Нужно разобраться.
            # Для прода вроде как не критично, т.к. боты будут работаь на вебхуках.
            await self.dp.stop_polling()

        if self.bot.session:
            await self.bot.session.close()
            logger.info(f"Bot '{self.name}' session closed.")

        logger.info(f"Bot '{self.name}' stopped.")
