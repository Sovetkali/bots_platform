from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from utils.config import config

class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self):
        self.engine = create_async_engine(
            url=config.get_db_url(),
            echo=True if config.DB_DEV_MODE else False,
            pool_size=5 if config.DB_DEV_MODE else 10,
            max_overflow=10 if config.DB_DEV_MODE else 20,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    def session(self):
        return self.session_factory()

db = Database()
