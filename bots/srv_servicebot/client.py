from core.clients.aiogram_client import AiogramBotClient
from core.models.client_config import BotClientConfig
from core.models.bot_mode import BotMode
from aiogram import Router
from utils.config import config

class ServiceBotClient(AiogramBotClient):
    name = "servicebot"

    def __init__(self, router: Router):
        super().__init__(
            name=self.name,
            config=BotClientConfig(
                token=config.SRV_SERVICEBOT_TOKEN.get_secret_value(),
                mode=BotMode.POLLING,
                webhook_url=None
            )
        )
        self.dp.include_router(router)
