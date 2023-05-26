import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.depends.db import get as get_db
from db import trucks as db_trucks

from models.base import SuccessResponse
from models.trucks import (
    TruckUpdate,
    TrucksListResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['trucks']
)


@router.get("/trucks", response_model=TrucksListResponse)
async def get_list_trucks(
        limit: int = 100,
        offset: int = 0,
        conn: db_trucks.db_model = Depends(get_db)
) -> TrucksListResponse:
    """Получение списка Машин с пагинацией"""
    trucks = await db_trucks.get_trucks_limited(
        conn=conn,
        limit=limit,
        offset=offset
    )
    return TrucksListResponse(
        total=len(trucks),
        trucks=trucks
    )


@router.put("/trucks/{truck_id}", response_model=SuccessResponse)
async def update_truck(
        truck_id: int,
        truck_update: TruckUpdate,
        conn: db_trucks.db_model = Depends(get_db)
) -> SuccessResponse:
    """Обновление локации Машины по её id"""
    result = await db_trucks.update_truck_location(conn, truck_id, truck_update.location_zip)
    if not result:
        raise HTTPException(status_code=422, detail="Incorrect input(truck_id or zipcode)")

    return SuccessResponse(data=result)
