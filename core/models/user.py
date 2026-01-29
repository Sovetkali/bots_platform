from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class User:
    id: int
    name: str
    lang: Optional[str] = "en"
