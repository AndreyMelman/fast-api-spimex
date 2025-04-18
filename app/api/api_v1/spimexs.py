from fastapi import APIRouter

from schemas.spimex import (
    SpimexTradingDate,
    Spimex,
)
from api.dependencies.params import (
    SpimexFiltersD,
    SpimexFiltersR,
    LimitDependency,
    OffsetDependency,
    SpimexCrud,
    CURRENT_LIMIT,
    CURRENT_OFFSET,
)
from core.redis import redis_client
from services.cache import redis_cache
from ulils.time_utils import get_seconds_until_1411

router = APIRouter(
    tags=["Spimex"],
)


@router.get(
    "/last_trading_dates/",
    response_model=list[SpimexTradingDate],
)
@redis_cache(redis_client, ttl=get_seconds_until_1411())
async def get_last_trading_dates(
    crud: SpimexCrud,
    limit: LimitDependency = CURRENT_LIMIT,
    offset: OffsetDependency = CURRENT_OFFSET,
):
    """
    Эндпоинт для получения последних дат торгов

    :param crud: сессия
    :param limit: обязательный параметр для получения последних дат
    :param offset: для пагинации
    :return: список дат в формате JSON
    """
    return await crud.get_last_trading_dates(
        limit=limit,
        offset=offset,
    )


@router.get(
    "/dynamics/",
    response_model=list[Spimex],
)
@redis_cache(redis_client, ttl=get_seconds_until_1411())
async def get_dynamics(
    crud: SpimexCrud,
    filters: SpimexFiltersD,
    limit: LimitDependency = CURRENT_LIMIT,
    offset: OffsetDependency = CURRENT_OFFSET,
):
    """
    Эндпоинт для получения фильтрованных данных торгов по дате

    :param crud: сессия
    :param filters: фильтрация данных, обязательные параметры start_date и end_date
    :param limit: параметр для получения последних дат
    :param offset: для пагинации
    :return: возвращает список отфильтрованных данных в формате JSON
    """
    return await crud.get_dynamics(
        filters=filters,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/results/",
    response_model=list[Spimex],
)
@redis_cache(redis_client, ttl=get_seconds_until_1411())
async def get_trading_results(
    crud: SpimexCrud,
    filters: SpimexFiltersR,
    limit: LimitDependency = CURRENT_LIMIT,
    offset: OffsetDependency = CURRENT_OFFSET,
):
    """
    Эндпоинт для получения фильтрованных данных торгов за последнюю дату
    :param crud: сессия
    :param filters: фильтрация данных, нет обязательных параметров
    :param limit: параметр для получения последних дат
    :param offset: для пагинации
    :return: возвращает список отфильтрованных данных в формате JSON
    """
    return await crud.get_trading_results(
        filters=filters,
        limit=limit,
        offset=offset,
    )
