from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)

    name = Column(String(255), nullable=False)

    users = relationship(
        "User",
        secondary="user_bots",
        back_populates="bots"
    )
