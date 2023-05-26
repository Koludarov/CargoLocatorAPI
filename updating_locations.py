import asyncio
import logging.config

import asyncpg

from db.trucks import update_all_trucks_locations

logging.config.fileConfig('etc/logging.conf')
logger = logging.getLogger('Location_updater')


async def update_locations_periodically():
    """
    Автоматическое обновление локаций всех
    машин раз в 3 минуты (локация меняется на другую случайную)
    """
    conn = await asyncpg.connect(
        database="locator_api_db",
        user="postgres",
        password="postgres",
        host="db"
    )
    while True:
        await update_all_trucks_locations(conn)
        logger.info("Trucks' locations updated")
        await asyncio.sleep(180)  # Sleep for 180 seconds (3 minutes)


if __name__ == "__main__":
    asyncio.run(update_locations_periodically())
