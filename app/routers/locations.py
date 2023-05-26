import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.depends.db import get as get_db
from db import locations as db_locations

from models.locations import (
    Location,
    LocationsListResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['locations']
)


@router.get("/locations", response_model=LocationsListResponse)
async def get_list_locations(
        limit: int = 100,
        offset: int = 0,
        conn: db_locations.db_model = Depends(get_db)
) -> LocationsListResponse:
    """Получение списка Локаций с пагинацией"""
    locations = await db_locations.get_locations(
        conn=conn,
        limit=limit,
        offset=offset
    )
    return LocationsListResponse(
        total=len(locations),
        locations=locations)


@router.get("/locations/{location_id}", response_model=Location)
async def get_list_locations(
        location_id: int,
        conn: db_locations.db_model = Depends(get_db)
) -> Location:
    """Получение Локации по её id"""
    location = await db_locations.get_location_by_id(
        conn=conn,
        location_id=location_id
    )
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location
