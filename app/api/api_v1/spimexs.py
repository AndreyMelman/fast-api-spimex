from fastapi import APIRouter

from schemas.spimex import (
    SpimexTradingDate,
    Spimex,
)
from api.dependencies.parametrs import (
    SpimexFilters,
    LimitDependency,
    OffsetDependency,
    SpimexCrud,
)

router = APIRouter(
    tags=["Spimex"],
)


@router.get("/last_trading_dates/", response_model=list[SpimexTradingDate])
async def get_last_trading_dates(
    crud: SpimexCrud,
    limit: LimitDependency,
    offset: OffsetDependency = None,
):
    return await crud.get_last_trading_dates(
        limit=limit,
        offset=offset,
    )


@router.get("/dynamics/", response_model=list[Spimex])
async def get_dynamics(
    crud: SpimexCrud,
    filters: SpimexFilters,
    limit: LimitDependency = None,
    offset: OffsetDependency = None,
):
    return await crud.get_dynamics(
        filters=filters,
        limit=limit,
        offset=offset,
    )
