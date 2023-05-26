from fastapi import APIRouter
from . import (
    cargos,
    locations,
    trucks,
)


def register_routers(app):
    router = APIRouter(prefix='/api/v1')

    router.include_router(
        cargos.router,
    )
    router.include_router(
        locations.router,
    )
    router.include_router(
        trucks.router,
    )

    app.include_router(router)
    return app
