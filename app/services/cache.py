import json
import hashlib
from fastapi.encoders import jsonable_encoder
from functools import wraps
from redis.asyncio import Redis

from typing import (
    Callable,
    Any,
    Awaitable,
)


def redis_cache(redis_client: Redis, ttl: int):
    def decorator(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            data_to_cache = jsonable_encoder(kwargs)
            filter_str = json.dumps(data_to_cache, sort_keys=True)
            hash_str = hashlib.md5(filter_str.encode()).hexdigest()
            cache_key = f"{func.__name__}:{hash_str}"

            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            json_data = jsonable_encoder(result)
            await redis_client.set(
                cache_key,
                json.dumps(json_data),
                ex=ttl,
            )
            return json_data

        return wrapper

    return decorator
