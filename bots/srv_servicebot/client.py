from core.clients.aiogram_client import AiogramBotClient
from core.models.client_config import BotClientConfig
from core.models.bot_mode import BotMode
from .router import ServiceBotRouter
from utils.config import config

class ServiceBotClient(AiogramBotClient):
    name = "servicebot"

    def __init__(self):
        super().__init__(
            name=self.name,
            config=BotClientConfig(
                token=config.SRV_SERVICEBOT_TOKEN.get_secret_value(),
                mode=BotMode.POLLING,
                webhook_url=None
            )
        )
        self._router = ServiceBotRouter()
        self.dp.include_router(self._router.router)
