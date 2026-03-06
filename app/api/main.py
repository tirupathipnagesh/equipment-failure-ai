from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.logger import app_logger


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    app.include_router(health_router, prefix=settings.API_V1_PREFIX)

    @app.on_event("startup")
    def startup_event():
        app_logger.info("Application is starting up...")

    @app.on_event("shutdown")
    def shutdown_event():
        app_logger.info("Application is shutting down...")

    return app


app = create_app()