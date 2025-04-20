import json
import hashlib
import logging

from fastapi.encoders import jsonable_encoder
from functools import wraps
from redis.asyncio import Redis

from typing import (
    Callable,
    Any,
    Awaitable,
)

log = logging.getLogger(__name__)


def make_cache_key(func_name: str, kwargs: dict) -> str:
    data_to_cache = jsonable_encoder(kwargs)
    filter_str = json.dumps(data_to_cache, sort_keys=True)
    hash_str = hashlib.md5(filter_str.encode()).hexdigest()
    return f"{func_name}:{hash_str}"


def redis_cache(redis_client: Redis, ttl: int):
    def decorator(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = None
            try:
                cache_key = make_cache_key(func.__name__, kwargs)
                cached = await redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception as e:
                log.warning(
                    "Redis unavailable (get). Skipping cache. Error: e".format(e=e)
                )

            result = await func(*args, **kwargs)

            try:
                if cache_key is None:
                    cache_key = make_cache_key(func.__name__, kwargs)
                json_data = jsonable_encoder(result)
                await redis_client.set(
                    cache_key,
                    json.dumps(json_data),
                    ex=ttl,
                )
            except Exception as e:
                log.warning(
                    "Redis unavailable (set). Could not cache. Error: e".format(e=e)
                )

            return result

        return wrapper

    return decorator
