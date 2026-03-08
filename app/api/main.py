from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.predict import router as predict_router
from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.core.logger import app_logger
from app.db.init_db import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(health_router, prefix=settings.API_V1_PREFIX)
    app.include_router(predict_router, prefix=settings.API_V1_PREFIX)
    app.include_router(chat_router, prefix=settings.API_V1_PREFIX)

    @app.on_event("startup")
    def startup_event():
        init_db()
        app_logger.info("Application is starting up...")

    @app.on_event("shutdown")
    def shutdown_event():
        app_logger.info("Application is shutting down...")

    return app


app = create_app()