import logging
import os

import asyncpg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


async def startup(app):
    app.db_pool = await asyncpg.create_pool(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    logger.info(f'Connected to DB')


async def shutdown(app):
    await app.db_pool.close()
