from typing import (
    Optional,
    Any,
)

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Any]
