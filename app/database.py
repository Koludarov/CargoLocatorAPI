import logging

import asyncpg

logger = logging.getLogger(__name__)


async def startup(app):
    app.db_pool = await asyncpg.create_pool(
        user="postgres",
        password="postgres",
        database="locator_api_db",
        host="db"
    )
    logger.info(f'Connected to DB')


async def shutdown(app):
    await app.db_pool.close()
