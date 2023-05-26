import logging

from fastapi import FastAPI

from . import routers
from app.database import startup, shutdown
from misc.insert_data import add_trucks_locations

logger = logging.getLogger(__name__)

app = FastAPI(
        title='CargoLocator',
)


@app.on_event("startup")
async def app_startup():
    logger.info('Starting process')
    register_routers(app)
    logger.info('Routers registered')
    app.conn = await startup(app)
    await add_trucks_locations(app.db_pool)
    logger.info('Service ready')


@app.on_event("shutdown")
async def app_shutdown():
    logger.info('Shutdown called')
    try:
        await shutdown(app)
        logger.info(f"REST API app shutdown executed")
    except:
        logger.exception('Shutdown crashed')


def register_routers(main_app):
    return routers.register_routers(main_app)
