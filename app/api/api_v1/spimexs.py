from fastapi import APIRouter

from schemas.spimex import (
    SpimexTradingDate,
    Spimex,
)
from api.dependencies.params import (
    SpimexFiltersD,
    SpimexFiltersR,
    PaginationDep,
    SpimexCrud,
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
    pagination: PaginationDep,
):
    """
    Эндпоинт для получения последних дат торгов

    :param crud: сессия
    :param pagination: принимает 2 параметра limit и offset,
    limit обязательный параметр для получения последних дат
    :return: список дат в формате JSON
    """
    return await crud.get_last_trading_dates(
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get(
    "/dynamics/",
    response_model=list[Spimex],
)
@redis_cache(redis_client, ttl=get_seconds_until_1411())
async def get_dynamics(
    crud: SpimexCrud,
    filters: SpimexFiltersD,
    pagination: PaginationDep,
):
    """
    Эндпоинт для получения фильтрованных данных торгов по дате

    :param crud: сессия
    :param filters: фильтрация данных, обязательные параметры start_date и end_date
    :param pagination: принимает 2 параметра limit и offset,
    limit обязательный параметр для получения последних дат
    :return: возвращает список отфильтрованных данных в формате JSON
    """
    return await crud.get_dynamics(
        filters=filters,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get(
    "/results/",
    response_model=list[Spimex],
)
@redis_cache(redis_client, ttl=get_seconds_until_1411())
async def get_trading_results(
    crud: SpimexCrud,
    filters: SpimexFiltersR,
    pagination: PaginationDep,
):
    """
    Эндпоинт для получения фильтрованных данных торгов за последнюю дату

    :param crud: сессия
    :param filters: фильтрация данных, обязательные параметры start_date и end_date
    :param pagination: принимает 2 параметра limit и offset,
    limit обязательный параметр для получения последних дат
    :return: возвращает список отфильтрованных данных в формате JSON
    """
    return await crud.get_trading_results(
        filters=filters,
        limit=pagination.limit,
        offset=pagination.offset,
    )
