import csv
import logging
import random
from typing import cast

import asyncpg

from db import locations as db_locations
from db import trucks as db_trucks
from etc.config import CSV_FILE_PATH
from models.cargos import Location
from models.trucks import Truck
from misc.generate import generate_unique_id
from misc import db_model

logger = logging.getLogger(__name__)


async def load_zip_codes(
        filepath: str,
        conn: asyncpg.Connection
) -> None:
    """Добавление Локаций из csv-файла, если ещё не добавлены"""
    amount_locations = await db_locations.count_location(conn)
    if amount_locations < 1:
        with open(filepath, 'r') as file:
            csv_reader = csv.DictReader(file)
            zip_codes = []
            for row in csv_reader:
                zip_code = Location(
                    city=row['city'],
                    state=row['state_name'],
                    zip_code=row['zip'],
                    latitude=row['lat'],
                    longitude=row['lng']
                )
                zip_codes.append(zip_code)
            await db_locations.insert_locations(conn, zip_codes)
            logger.info(f'Inserted all rows')
            return

    logger.info(f'Locations already added')


async def add_trucks(conn: asyncpg.Connection) -> None:
    """Добавление 20 Машин, если ещё не добавлены"""
    amount_trucks = await db_trucks.count_trucks(conn)
    if amount_trucks < 1:
        trucks = []
        amount_locations = await db_locations.count_location(conn)
        for i in range(20):
            location_id = random.randint(1, amount_locations)
            trucks.append(
                Truck(
                    uuid=generate_unique_id(),
                    location_id=location_id,
                    capacity=random.randint(1, 1000))
            )
        await db_trucks.insert_trucks(conn, trucks)
        return

    logger.info(f'Trucks already added')


async def add_trucks_locations(conn: db_model.Pool) -> None:
    async with cast(asyncpg.pool.Pool, conn).acquire() as connection:
        await load_zip_codes(CSV_FILE_PATH, connection)
        await add_trucks(connection)
