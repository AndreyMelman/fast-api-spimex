import logging

from fastapi import FastAPI, Request, status

from pydantic import ValidationError
from starlette.responses import JSONResponse
from sqlalchemy import DatabaseError


log = logging.getLogger(__name__)

def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Unhandled error",
                "error": exc.errors(),
            },
        )

    @app.exception_handler(DatabaseError)
    def handle_db_error(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        log.error(
            "Unhandled database error",
            exc_info=exc,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error has occurred. "
                           "Our admins are already working on it."
            },
        )