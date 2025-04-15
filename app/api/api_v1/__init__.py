from fastapi import APIRouter

from core.config import settings
from .spimexs import router as spimex_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(spimex_router, prefix=settings.api.v1.spimex)
