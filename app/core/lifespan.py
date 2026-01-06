from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.redis import init_redis, close_redis
from app.core.rate_limiter import init_rate_limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()

    if redis:
        await init_rate_limiter(redis)

    yield

    await close_redis()
