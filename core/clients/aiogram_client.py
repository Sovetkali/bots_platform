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
        await self.bot.session.close()
