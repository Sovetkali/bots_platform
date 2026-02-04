from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from core.database import Base

class UserBot(Base):
    __tablename__ = "user_bots"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey(("users.id"), ondelete="CASCADE"))
    bot_id = Column(Integer, ForeignKey(("bots.id"), ondelete="CASCADE"))

    first_used_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "bot_id", name="uq_user_bot"),
    )
