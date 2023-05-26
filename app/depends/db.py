import logging

import fastapi

from misc import db_model

logger = logging.getLogger(__name__)


async def get(request: fastapi.Request) -> db_model.Connection:
    try:
        pool = request.app.db_pool
    except AttributeError:
        raise RuntimeError('Application has no db pool')
    else:
        async with pool.acquire() as conn:
            yield conn
