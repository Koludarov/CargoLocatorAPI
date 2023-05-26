from typing import Optional, List

from pydantic import BaseModel

from models.locations import Location


class Truck(BaseModel):
    id: Optional[int]
    uuid: str
    location_id: int
    capacity: int


class TruckUpdate(BaseModel):
    location_zip: str


class TruckDistance(BaseModel):
    truck_id: str
    capacity: int
    distance: float


class TrucksDistanceList(BaseModel):
    total: int
    trucks_available: List[TruckDistance]
    trucks_not_enough_space: List[TruckDistance]


class TruckResponse(BaseModel):
    id: Optional[int]
    uuid: str
    location: Location
    capacity: int


class TrucksListResponse(BaseModel):
    total: int
    trucks: List[TruckResponse]
