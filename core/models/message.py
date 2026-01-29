from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    msg_id: int
    date: datetime
    chat_id: int
    text: str
