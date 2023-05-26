from typing import List, Optional

from pydantic import BaseModel, Field

from models.trucks import TrucksDistanceList
from models.locations import Location


class Cargo(BaseModel):
    id: Optional[int]
    pickup_location_id: str
    delivery_location_id: str
    weight: int = Field(..., ge=0, le=1000)
    description: str


class CargoBase(BaseModel):
    id: int
    pickup_location_id: str
    delivery_location_id: str
    weight: int
    description: str


class CargoCreate(BaseModel):
    pickup_zip: str
    delivery_zip: str
    weight: int = Field(..., ge=0, le=1000)
    description: str


class CargoUpdate(BaseModel):
    weight: Optional[int] = Field(..., ge=0, le=1000)
    description: Optional[str]


class CargoResponse(BaseModel):
    cargo: Cargo
    trucks_info: TrucksDistanceList


class CargoSingleResponse(BaseModel):
    id: Optional[int]
    pickup_location: Location
    delivery_location: Location
    weight: int
    description: str
    trucks: TrucksDistanceList


class CargoListResponse(BaseModel):
    total: int
    items: List[CargoResponse]
