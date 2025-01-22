from fastapi import FastAPI

from src.api.lifespan import run_migrations
from src.api.routers.organization_router import router as organization_router


def get_app():
    app = FastAPI(
        title="API",
    )
    app.include_router(organization_router)

    @app.on_event("startup")
    async def on_startup():
        await run_migrations()

    @app.get("/")
    async def healthcheck() -> dict[str, bool]:
        return {"Success": True}

    return app
