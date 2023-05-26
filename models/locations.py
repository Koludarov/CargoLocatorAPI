from typing import Optional, List

from pydantic import BaseModel


class Location(BaseModel):
    id: Optional[int]
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float


class LocationResponse(BaseModel):
    id: int
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float


class LocationsListResponse(BaseModel):
    total: int
    locations: List[LocationResponse]
