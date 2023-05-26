import logging
from typing import List, Optional

from misc import db_model

from models.locations import (
    Location,
    LocationResponse
)

logger = logging.getLogger(__name__)


async def count_location(conn: db_model.Connection,) -> int:
    """Подсчёт количества Локаций"""
    async with conn.transaction():
        result = await conn.fetchrow(f"SELECT COUNT(*) as count FROM locations")
        return result['count']


async def create_location(
        conn: db_model.Connection,
        location: Location
) -> int:
    """Добавление одной Локации"""
    async with conn.transaction():
        location_id = await conn.fetchrow(
            "INSERT INTO locations (city, state, zip_code, latitude, longitude) "
            "VALUES ($1, $2, $3, $4, $5) RETURNING id",
            location.city, location.state, location.zip_code, location.latitude, location.longitude
        )
        return location_id


async def insert_locations(
        conn: db_model.Connection,
        locations: List[Location]
) -> None:
    """Добавление списка Локаций"""
    async with conn.transaction():
        values = [(location.city,
                   location.state,
                   location.zip_code,
                   location.latitude,
                   location.longitude)
                  for location in locations]
        query = "INSERT INTO locations (city, state, zip_code, latitude, longitude) VALUES ($1, $2, $3, $4, $5)"
        await conn.executemany(query, values)


async def get_locations(
        conn: db_model.Connection,
        offset: int,
        limit: int
) -> Optional[List[LocationResponse]]:
    """Получение списка Локаций с пагинацией, для снижения нагрузки на БД"""
    async with conn.transaction():
        locations = await conn.fetch(
            f"SELECT * FROM locations OFFSET {offset} LIMIT {limit}"
        )
        return db_model.record_to_model_list(LocationResponse, locations)


async def get_location_by_id(
        conn: db_model.Connection,
        location_id: int
) -> Location:
    """Получение Локации по её id"""
    async with conn.transaction():
        location = await conn.fetchrow(
            f"SELECT * FROM locations WHERE id={location_id}"
        )
        return db_model.record_to_model(Location, location)


async def get_location_by_zip(
        conn: db_model.Connection,
        zip_code: str
) -> Location:
    """Получение Локации по её zipcode"""
    async with conn.transaction():
        location = await conn.fetchrow(
            f"SELECT * FROM locations WHERE zip_code='{zip_code}'"
        )

        return db_model.record_to_model(Location, location)
