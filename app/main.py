import logging
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from core.models import db_helper
from ulils.common_log import configure_logging

from api import router as api_router
from ulils.errors_handlers import register_error_handlers

configure_logging(level=logging.INFO)
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router)
register_error_handlers(main_app)

@main_app.get("/")
async def root():
    return {"message": "Hello"}


if __name__ == "__main__":
    log.info("Starting application")

    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
