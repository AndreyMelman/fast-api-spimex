import redis.asyncio as redis
from core.config import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    decode_responses=settings.redis.decode_responses,
)
