from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings
from app.core.validation import validation_exception_handler
from app.middleware.response_middleware import UniversalResponseMiddleware
from app.core.cors import setup_cors
from app.middleware.logging_middleware import LoggingMiddleware


app = FastAPI(title=settings.APP_NAME)
origins = origins = settings.CORS_ORIGINS.split(",")

# Middlewares
setup_cors(app, origins)
app.add_middleware(LoggingMiddleware)
app.add_middleware(UniversalResponseMiddleware)

# Exception Handlers
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

app.include_router(api_router)
