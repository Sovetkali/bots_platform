from logging.config import fileConfig
import logging

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from core.database import db, Base
from core.models.db.user import User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Добавляем логирование для диагностики
logger = logging.getLogger('alembic.env')

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    logger.info("Running migrations in OFFLINE mode")

    # Получаем URL из конфигурации alembic.ini
    url = config.get_main_option("sqlalchemy.url")
    logger.info(f"URL from alembic.ini: {url}")

    if not url or url == "driver://user:pass@localhost/dbname":
        # Если URL не настроен, используем URL из нашей конфигурации
        from utils.config import config as app_config
        url = app_config.get_db_url()
        logger.info(f"Using app config URL: {url}")

    # Заменяем asyncpg на psycopg2 для синхронного подключения
    url = url.replace("+asyncpg", "+psycopg2")
    logger.info(f"Final URL: {url}")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    logger.info("Running migrations in ONLINE mode")

    # Получаем конфигурацию из alembic.ini
    section = config.get_section(config.config_ini_section, {})
    logger.info(f"Config section: {section}")

    # Если URL не настроен, используем URL из нашей конфигурации
    if not section.get('sqlalchemy.url') or section.get('sqlalchemy.url') == "driver://user:pass@localhost/dbname":
        from utils.config import config as app_config
        section['sqlalchemy.url'] = app_config.get_db_url().replace("+asyncpg", "+psycopg2")
        logger.info(f"Using app config URL: {section['sqlalchemy.url']}")

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"sslmode": "prefer", "gssencmode": "disable"}
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
