from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Conflict error", "exc": exc.orig.__dict__}
        )

    @app.exception_handler(NoResultFound)
    async def integrity_exception_handler(request: Request, exc: NoResultFound):
        return JSONResponse(
            status_code=404,
            content={"detail": 'Not found error'}
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content={"detail": "A database error occurred.", "exc": f"{exc}"}
        )
