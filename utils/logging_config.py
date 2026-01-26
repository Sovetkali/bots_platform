from pathlib import Path
from dataclasses import dataclass
from aiogram import Bot
from .config import config

@dataclass
class LoggingConfig:
    ENV: bool = config.DEV_MODE
    LOGS_DIR: str = Path(__file__).parent.parent / "logs"

    SRV_BOT: Bot = Bot(token=config.SRV_SERVICEBOT_TOKEN.get_secret_value())
    SRV_CHAT_ID: str = config.SERVICE_CHAT_ID


log_config = LoggingConfig()
