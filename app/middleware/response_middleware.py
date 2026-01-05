# app/middleware/universal_response.py
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
import json

class UniversalResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)

            # Only wrap JSON responses
            if "application/json" in response.headers.get("content-type", ""):
                body_bytes = b""
                async for chunk in response.body_iterator:
                    body_bytes += chunk

                body_content = json.loads(body_bytes.decode())

                success = 200 <= response.status_code < 300
                universal_body = {
                    "status": response.status_code,
                    "success": success,
                }

                if success:
                    universal_body["body"] = body_content
                else:
                    universal_body["error"] = body_content

                return JSONResponse(
                    status_code=response.status_code,
                    content=universal_body,
                )

            return response

        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "status": e.status_code,
                    "success": False,
                    "error": e.detail,
                }
            )
        except RequestValidationError as e:
            return JSONResponse(
                status_code=422,
                content={
                    "status": 422,
                    "success": False,
                    "error": e.errors(),
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "status": 500,
                    "success": False,
                    "error": str(e),
                }
            )
