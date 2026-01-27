from pydantic import BaseModel
from core.models.bot_mode import BotMode

class BotClientConfig(BaseModel):
    token: str
    mode: BotMode
    webhook_url: str | None = None
