from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Optional

class Config(BaseSettings):
    DEV_MODE: Optional[bool] = False
    SERVICE_CHAT_ID: Optional[str] = None
    SRV_SERVICEBOT_TOKEN: SecretStr

    DB_DEV_MODE: Optional[bool] = True
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_ENGINE: str = "postgresql"

    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )

    def get_db_url(self):
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

config = Config()
