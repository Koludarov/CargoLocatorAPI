import logging
import random
from typing import List, Optional

from db import locations as db_locations
from misc.consts import DISTANCE_LESS, DISTANCE_MORE
from misc import db_model
from misc.generate import calculate_distance
from models.locations import Location
from models.trucks import (
    Truck,
    TruckDistance,
    TruckResponse,
    TrucksDistanceList
)

logger = logging.getLogger(__name__)


async def count_trucks(conn: db_model.Connection, ) -> int:
    """Подсчёт количества Машин"""
    async with conn.transaction():
        result = await conn.fetchrow(f"SELECT COUNT(*) as count FROM trucks")
        return result['count']


async def insert_trucks(
        conn: db_model.Connection,
        trucks: List[Truck]
) -> None:
    """Добавление списка Машин"""
    async with conn.transaction():
        values = [(truck.uuid, truck.location_id, truck.capacity) for truck in trucks]
        query = "INSERT INTO trucks (uuid, location_id, capacity) VALUES ($1, $2, $3)"
        await conn.executemany(query, values)


async def get_all_trucks(conn: db_model.Connection) -> Optional[List[Truck]]:
    """Получение списка Машин с пагинацией, для снижения нагрузки на БД"""
    async with conn.transaction():
        page_size = 100
        offset = 0

        all_trucks = []
        while True:
            query = f"SELECT * FROM trucks LIMIT {page_size} OFFSET {offset}"
            trucks = await conn.fetch(query)
            if not trucks:
                break
            all_trucks.extend(db_model.record_to_model_list(Truck, trucks))
            offset += page_size

        return all_trucks


async def get_trucks_limited(
        conn: db_model.Connection,
        offset: int,
        limit: int
) -> Optional[List[TruckResponse]]:
    """Получение списка Машин с пагинацией, с подробными Локациями"""
    async with conn.transaction():
        trucks = []
        trucks_records = await conn.fetch(
            """SELECT
            n.id as location_id, n.city AS location_city, n.state AS location_state, n.zip_code AS location_zip_code,
            n.latitude AS location_latitude, n.longitude AS location_longitude,
            t.id, t.uuid, t.capacity
            FROM trucks t
            JOIN locations n ON t.location_id = n.id
            OFFSET $1 LIMIT $2""",
            offset, limit
        )
        for truck in trucks_records:
            trucks.append(TruckResponse(
                id=truck['id'],
                uuid=truck['uuid'],
                location=Location(
                    id=truck['location_id'],
                    city=truck['location_city'],
                    state=truck['location_state'],
                    zip_code=truck['location_zip_code'],
                    latitude=truck['location_latitude'],
                    longitude=truck['location_longitude']
                ),
                capacity=truck['capacity']))

        return trucks


async def get_trucks_list(
        conn: db_model.Connection,
        location_id: str,
        weight: int
) -> Optional[TrucksDistanceList]:
    """
    Функция для одноразового получения полного списка Машин и передачи его в get_distance_trucks_info
    Возвращение списка TruckDistanceList
    """
    trucks_list = await get_all_trucks(conn=conn)
    trucks = await get_distance_trucks_info(conn, location_id, trucks_list, weight=weight)
    return trucks


async def get_distance_trucks_info(
        conn: db_model.Connection,
        location_id: str,
        trucks_list: List[Truck],
        distance_less: int = None,
        distance_more: int = None,
        weight: int = None
) -> Optional[TrucksDistanceList]:
    """
    Получение списка TruckDistanceList(Общее количество Машин;
                                       доступные Машины;
                                       Машины, у которых нет места для Груза)
                     TruckDistance(уникальный номер машины;
                                   вместимость;
                                   расстояние до Груза)
       С возможностью фильтрации:
       - distance_more больше, чем n миль
       - distance_less меньше, чем n миль
       По умолчанию получает полный список
    """
    async with conn.transaction():
        distance_more = distance_more if distance_more is not None else DISTANCE_MORE
        distance_less = distance_less if distance_less is not None else DISTANCE_LESS

        trucks_less = []
        trucks_more = []
        location = await db_locations.get_location_by_id(conn, int(location_id))

        for truck in trucks_list:
            truck_location = await db_locations.get_location_by_id(conn, truck.location_id)
            distance = await calculate_distance(location, truck_location)
            if distance <= distance_less:
                trucks_less.append(TruckDistance(
                    truck_id=truck.uuid,
                    capacity=truck.capacity,
                    distance=distance)
                )

            if distance >= distance_more:
                trucks_more.append(TruckDistance(
                    truck_id=truck.uuid,
                    capacity=truck.capacity,
                    distance=distance)
                )

        the_nearest_trucks = [truck for truck in trucks_less if truck in trucks_more]
        return TrucksDistanceList(
            total=len(the_nearest_trucks),
            trucks_available=[truck for truck in the_nearest_trucks if truck.capacity >= weight],
            trucks_not_enough_space=[truck for truck in the_nearest_trucks if truck.capacity < weight]
        )


async def update_truck_location(
        conn: db_model.Connection,
        truck_id: int,
        zip_code: str
) -> Optional[Truck]:
    """Обновление локации Машины по её id"""
    async with conn.transaction():
        location = await db_locations.get_location_by_zip(conn, zip_code)
        truck = await conn.fetchrow(
            "UPDATE trucks SET location_id = $1 WHERE id = $2 RETURNING *",
            location.id, truck_id
        )
        return db_model.record_to_model(Truck, truck)


async def update_all_trucks_locations(conn: db_model.Connection):
    """Обновление локаций у всех Машин"""
    async with conn.transaction():
        trucks = await conn.fetch('SELECT id FROM trucks')
        for truck in trucks:
            amount_locations = await db_locations.count_location(conn)
            new_location_id = random.randint(1, amount_locations)
            await conn.execute('UPDATE trucks SET location_id = $1 WHERE id = $2', new_location_id, truck['id'])
        return True
