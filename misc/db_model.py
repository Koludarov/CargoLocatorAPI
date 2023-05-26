from typing import Type, Optional, List

import asyncpg

from pydantic import BaseModel

Pool = asyncpg.Pool
Connection = asyncpg.Connection


def record_to_model(model_cls: Type[BaseModel], record: Optional[asyncpg.Record]) -> Optional[BaseModel]:
    if record:
        return model_cls.parse_obj(record)
    return None


def record_to_model_list(model_cls: Type[BaseModel], records: List[asyncpg.Record]) -> List[BaseModel]:
    if records:
        return [record_to_model(model_cls, i) for i in records]
    return []
