from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.main import protected_router, public_router
from app.core.config import settings
from app.core.validation import validation_exception_handler
from app.middleware.response_middleware import UniversalResponseMiddleware
from app.core.cors import setup_cors
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.lifespan import lifespan
from app.dependencies.auth import get_current_user
from app.dependencies.rate_limit import rate_limit_dependency
from app.tasks.email import send_email

app = FastAPI(title=settings.APP_NAME,lifespan=lifespan)
origins = settings.CORS_ORIGINS.split(",")

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


# celeryy test 
@app.post("/celery-test")
def celery_test(email: str):
    task = send_email.delay(email)
    return {
        "message": "Task submitted",
        "task_id": task.id
    }

# Public APIs (no auth)
app.include_router(public_router)

# Protected APIs (auth + rate limit)
app.include_router(
    protected_router,
    dependencies=[
        Depends(get_current_user),
        Depends(rate_limit_dependency),

    ],
)
