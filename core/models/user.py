from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class User:
    tg_id: int
    name: str
    lang: Optional[str] = "en"
