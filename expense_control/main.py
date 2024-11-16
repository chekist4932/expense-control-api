from fastapi import FastAPI
from contextlib import asynccontextmanager

from expense_control.exceptions import register_exception_handlers
from database import session_manager
from config import get_db_settings, get_app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init(get_db_settings().DATABASE_URI)
    yield
    await session_manager.close()


app = FastAPI(title=get_app_settings().APP_NAME, lifespan=lifespan)

register_exception_handlers(app)
