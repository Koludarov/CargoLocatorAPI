import asyncio
import logging.config
import os

import asyncpg
from dotenv import load_dotenv

from db.trucks import update_all_trucks_locations

logging.config.fileConfig('etc/logging.conf')
logger = logging.getLogger('Location_updater')

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


async def update_locations_periodically():
    """
    Автоматическое обновление локаций всех
    машин раз в 3 минуты (локация меняется на другую случайную)
    """
    conn = await asyncpg.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    while True:
        await asyncio.sleep(180)
        await update_all_trucks_locations(conn)
        logger.info("Trucks' locations updated")


if __name__ == "__main__":
    asyncio.run(update_locations_periodically())
