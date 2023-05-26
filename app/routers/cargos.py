import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.depends.db import get as get_db
from db import cargos as db_cargos
from db import trucks as db_trucks

from misc.consts import DISTANCE_USUAL
from models.cargos import (
    CargoCreate,
    CargoUpdate,
    CargoResponse,
    CargoSingleResponse,
    CargoListResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['cargos']
)


@router.post("/cargos", response_model=CargoResponse)
async def create_new_cargo(
        cargo_data: CargoCreate,
        conn: db_trucks.db_model = Depends(get_db)
) -> CargoResponse:
    """
    Создание нового груза (характеристики локаций pick-up,
    delivery определяются по введенному zip-коду)
    """
    cargo = await db_cargos.create_cargo(conn, cargo_data)
    if not cargo:
        raise HTTPException(status_code=422, detail="Incorrect input zipcode")

    return CargoResponse(
        cargo=cargo,
        trucks_info=await db_trucks.get_trucks_list(
            conn,
            cargo.pickup_location_id,
            cargo.weight)
    )


@router.get("/cargos", response_model=CargoListResponse)
async def get_all_cargos(
        conn: db_trucks.db_model = Depends(get_db)
) -> CargoListResponse:
    """
    Получение списка грузов (локации pick-up, delivery,
    количество ближайших машин до груза ( =< 450 миль))
    """
    cargos = await db_cargos.filter_cargos(
        conn,
        distance_less=DISTANCE_USUAL
    )
    return CargoListResponse(
        total=len(cargos),
        items=cargos
    )


@router.get("/cargos_filtered", response_model=CargoListResponse)
async def get_cargos_filtered(
        weight_more: int = None,
        weight_less: int = None,
        distance_more: int = None,
        distance_less: int = None,
        conn: db_cargos.db_model = Depends(get_db)
) -> CargoListResponse:
    """Фильтр списка грузов (вес, мили ближайших машин до грузов)"""
    cargos = await db_cargos.filter_cargos(
        conn,
        weight_more=weight_more,
        weight_less=weight_less,
        distance_more=distance_more,
        distance_less=distance_less
    )
    return CargoListResponse(
        total=len(cargos),
        items=cargos
    )


@router.get("/cargos/{cargo_id}", response_model=CargoSingleResponse)
async def get_cargo_by_id(
        cargo_id: int,
        conn: db_trucks.db_model = Depends(get_db)
) -> CargoSingleResponse:
    """
    Получение информации о конкретном грузе
    по ID (локации pick-up, delivery, вес, описание,
    список номеров ВСЕХ машин с расстоянием до выбранного груза)
    """
    cargo = await db_cargos.get_cargo(conn, cargo_id)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    return cargo


@router.put("/cargos/{cargo_id}", status_code=204)
async def update_cargo_by_id(
        cargo_id: int,
        cargo_update: CargoUpdate,
        conn: db_trucks.db_model = Depends(get_db)
) -> None:
    """Обновление веса и описания Груза по его id"""
    await db_cargos.update_cargo(conn, cargo_id, cargo_update)


@router.delete("/cargos/{cargo_id}", status_code=204)
async def delete_cargo_by_id(
        cargo_id: int,
        conn: db_trucks.db_model = Depends(get_db)
) -> None:
    """Удаление Груза по его id"""
    await db_cargos.delete_cargo(conn, cargo_id)
