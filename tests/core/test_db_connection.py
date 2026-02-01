import pytest
import asyncpg
from utils.config import config

@pytest.mark.integration
# run test: pytest -m integration
@pytest.mark.asyncio
async def test_postgres_connection():
    conn = await asyncpg.connect(
        user=config.DB_USER,
        password=config.DB_PASSWORD.get_secret_value(),
        database=config.DB_NAME,
        host=config.DB_HOST,
        port=int(config.DB_PORT),
    )

    result = await conn.fetchval("SELECT 1;")
    await conn.close()

    assert result == 1
