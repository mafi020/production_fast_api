import logging
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

redis: Redis | None = None


async def init_redis():
    global redis

    if not settings.REDIS_HOST:
        logger.warning("Redis is not configured. Rate limiting disabled.")
        return None

    try:
        redis = Redis.from_url(
            settings.REDIS_HOST,
            decode_responses=True,
        )

        await redis.ping()
        logger.info("Redis connected successfully")

    except Exception as e:
        logger.warning(f"Redis unavailable ({e}). Rate limiting disabled.")
        redis = None

    return redis


async def close_redis():
    global redis
    if redis:
        await redis.close()
        redis = None
