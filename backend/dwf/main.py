from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from dwf.infrastructure.database.engine import create_engine, create_session_factory
from dwf.infrastructure.observability.logging import setup_logging
from dwf.settings import Settings

logger = structlog.stdlib.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings
    setup_logging(settings.log_level)

    engine = create_engine(settings.database_url)
    app.state.engine = engine
    app.state.session_factory = create_session_factory(engine)

    logger.info("startup_complete", database=settings.database_url.split("@")[-1])
    yield

    await engine.dispose()
    logger.info("shutdown_complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = Settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    app.state.settings = settings

    from dwf.api.routers.health import router as health_router

    app.include_router(health_router)

    return app


app = create_app()
