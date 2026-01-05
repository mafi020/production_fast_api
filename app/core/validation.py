from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


def format_validation_errors(exc: RequestValidationError) -> dict:
    errors: dict[str, str] = {}

    for error in exc.errors():
        loc = error["loc"]

        # We only care about body fields
        if loc[0] == "body":
            field = loc[-1]

            message = error["msg"]

            # Optional: make messages nicer
            if message == "Field required":
                message = f"{field.replace('_', ' ').title()} is required"

            errors[field] = message

    return errors


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_validation_errors(exc),
    )
