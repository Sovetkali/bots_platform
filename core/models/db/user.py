from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True, index=True)

    name = Column(String(255), nullable=False)
    lang = Column(String(10), default="en")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bots = relationship(
        "Bot",
        secondary="user_bots",
        back_populates="users"
    )
