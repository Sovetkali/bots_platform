from enum import Enum

class BotMode(str, Enum):
    POLLING = "polling"
    WEBHOOK = "webhook"
