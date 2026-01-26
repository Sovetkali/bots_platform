from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Optional

class Config(BaseSettings):
    DEV_MODE: Optional[bool] = False
    SERVICE_CHAT_ID: Optional[str] = None
    SRV_SERVICEBOT_TOKEN: SecretStr

    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )


config = Config()
