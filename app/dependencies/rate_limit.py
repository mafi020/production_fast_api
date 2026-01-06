from fastapi import Request
from fastapi_limiter.depends import RateLimiter
from app.core.redis import redis


async def rate_limit_dependency(request: Request):
    """
    Applies rate limiting only if Redis is available.
    Otherwise does nothing.
    """
    if redis is None:
        return

    limiter = RateLimiter(times=100, seconds=60)
    await limiter(request)
