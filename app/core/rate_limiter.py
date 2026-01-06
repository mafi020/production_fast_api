from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
import logging

logger = logging.getLogger(__name__)


async def init_rate_limiter(redis: Redis):
    try:
        await FastAPILimiter.init(redis)
        logger.info("Rate limiter enabled")
    except Exception as e:
        logger.warning(f"Rate limiter disabled: {e}")
