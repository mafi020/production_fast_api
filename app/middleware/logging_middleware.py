from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from app.core.logging import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response: Response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)
        logger.info(
            f"{request.method} {request.url} - {response.status_code} - {duration}ms"
        )
        return response
