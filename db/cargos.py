import logging
from typing import List, Optional

from db import locations as db_locations
from db import trucks as db_trucks
from misc import db_model

from models.locations import (
    Location
)
from models.cargos import (
    Cargo,
    CargoCreate,
    CargoUpdate,
    CargoSingleResponse,
    CargoResponse
)

logger = logging.getLogger(__name__)


async def create_cargo(
        conn: db_model.Connection,
        cargo: CargoCreate
) -> Optional[Cargo]:
    async with conn.transaction():
        pickup_location = await db_locations.get_location_by_zip(
            conn=conn,
            zip_code=cargo.pickup_zip
        )
        if not pickup_location:
            return None
        delivery_location = await db_locations.get_location_by_zip(
            conn=conn,
            zip_code=cargo.delivery_zip
        )
        if not delivery_location:
            return None

        cargo_data = await conn.fetchrow(
            """INSERT INTO cargos (pickup_location_id, delivery_location_id, weight, description)
            VALUES ($1, $2, $3, $4) RETURNING *""",
            pickup_location.id, delivery_location.id, cargo.weight, cargo.description
        )

        return db_model.record_to_model(Cargo, cargo_data)


async def get_cargos(
        conn: db_model.Connection,
) -> Optional[List[Cargo]]:
    """Получение списка Грузов с пагинацией, для снижения нагрузки на БД"""
    async with conn.transaction():
        page_size = 100
        offset = 0

        all_cargos = []
        while True:
            query = f"SELECT * FROM cargos LIMIT {page_size} OFFSET {offset}"
            cargos = await conn.fetch(query)
            if not cargos:
                break
            all_cargos.extend(db_model.record_to_model_list(Cargo, cargos))
            offset += page_size

        return all_cargos


async def get_cargo(
        conn: db_model.Connection,
        cargo_id: int
) -> Optional[CargoSingleResponse]:
    """Получение Груза, с подробными Локациями и расстоянием Машин до него, по id"""
    async with conn.transaction():
        cargo = await conn.fetchrow(
            """SELECT c.id, 
            p.id as pickup_id, p.city AS pickup_city, p.state AS pickup_state, p.zip_code AS pickup_zip_code,
            p.latitude AS pickup_latitude, p.longitude AS pickup_longitude,
            d.id as delivery_id, d.city AS delivery_city, d.state AS delivery_state, d.zip_code AS delivery_zip_code,
            d.latitude AS delivery_latitude, d.longitude AS delivery_longitude,
            c.weight, c.description
            FROM cargos c
            JOIN locations p ON c.pickup_location_id = p.id
            JOIN locations d ON c.delivery_location_id = d.id
            WHERE c.id = $1""",
            cargo_id
        )

        if not cargo:
            return None

        pickup_location = Location(
            id=cargo['pickup_id'],
            city=cargo['pickup_city'],
            state=cargo['pickup_state'],
            zip_code=cargo['pickup_zip_code'],
            latitude=cargo['pickup_latitude'],
            longitude=cargo['pickup_longitude']
        )
        delivery_location = Location(
            id=cargo['delivery_id'],
            city=cargo['delivery_city'],
            state=cargo['delivery_state'],
            zip_code=cargo['delivery_zip_code'],
            latitude=cargo['delivery_latitude'],
            longitude=cargo['delivery_longitude']
        )

        return CargoSingleResponse(
            id=cargo['id'],
            pickup_location=pickup_location,
            delivery_location=delivery_location,
            weight=cargo['weight'],
            description=cargo['description'],
            trucks=await db_trucks.get_trucks_list(conn,
                                                   cargo['pickup_id'],
                                                   weight=cargo['weight'])
        )


async def update_cargo(
        conn: db_model.Connection,
        cargo_id: int,
        cargo: CargoUpdate
) -> Optional[Cargo]:
    """Обновление веса и описания Груза по id"""
    async with conn.transaction():
        cargo = await conn.fetchrow(
            """UPDATE cargos SET weight = $1, description = $2 WHERE id = $3
                RETURNING *
            """,
            cargo.weight, cargo.description, cargo_id
        )
        return db_model.record_to_model(Cargo, cargo)


async def delete_cargo(
        conn: db_model.Connection,
        cargo_id: int
) -> Optional[Cargo]:
    """Удаление Груза по id"""
    async with conn.transaction():
        cargo = await conn.fetchrow(
            "DELETE FROM cargos WHERE id = $1 RETURNING *",
            cargo_id
        )
        return db_model.record_to_model(Cargo, cargo)


async def filter_cargos(
        conn: db_model.Connection,
        weight_more: int = None,
        weight_less: int = None,
        distance_more: int = None,
        distance_less: int = None
) -> List[CargoResponse]:
    """Получение Грузов, с фильтрацией:
    - вес(больше, меньше),
    - мили ближайших машин до грузов(больше, меньше)
    По умолчанию получаем все Грузы"""
    async with conn.transaction():
        cargos_response = []
        query = 'SELECT * FROM cargos WHERE 1=1'

        if weight_more:
            query += f' AND weight >= {weight_more}'

        if weight_less:
            query += f' AND weight <= {weight_less}'

        cargos = await conn.fetch(query)

        trucks_list = await db_trucks.get_all_trucks(conn)

        for cargo in cargos:
            trucks = await db_trucks.get_distance_trucks_info(
                conn,
                cargo['pickup_location_id'],
                trucks_list,
                distance_less=distance_less,
                distance_more=distance_more,
                weight=cargo['weight']
            )

            if trucks.total > 0:
                cargos_response.append(CargoResponse(
                    cargo=cargo,
                    trucks_info=trucks
                ))

        return cargos_response
