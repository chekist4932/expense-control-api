from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content={"detail": "A database error occurred.", "exc": f"{exc}"}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
