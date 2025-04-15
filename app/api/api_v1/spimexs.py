from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from crud.spimexs import SpimexCRUD

from schemas.spimex import SpimexTradingDate, SpimexFiltersBase, Spimex
from .dependencies import spimex_crud

router = APIRouter(
    tags=["Spimex"],
)

SpimexFilters = Annotated[SpimexFiltersBase, Depends()]
LimitDependency = Annotated[int, Query()]
OffsetDependency = Annotated[int, Query()]

@router.get("/", response_model=list[SpimexTradingDate])
async def get_last_trading_dates(
    crud: Annotated[SpimexCRUD, Depends(spimex_crud)],
    limit: LimitDependency,
    offset: OffsetDependency = None,
):
    return await crud.get_last_trading_dates(
        limit=limit,
        offset=offset,
    )


@router.get("/dynamics", response_model=list[Spimex])
async def get_dynamics(
    crud: Annotated[SpimexCRUD, Depends(spimex_crud)],
    filters: SpimexFilters,
    limit: LimitDependency = None,
    offset: OffsetDependency = None,
):
    return await crud.get_dynamics(
        filters=filters,
        limit=limit,
        offset=offset,
    )
