import asyncio

from uvicorn import Config, Server

from fastapi import FastAPI
from contextlib import asynccontextmanager

from expense_control.exceptions import register_exception_handlers
from expense_control.database import session_manager
from expense_control.config import get_db_settings, get_app_settings

from expense_control.expense import expense_router
from expense_control.category import category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init(get_db_settings().DATABASE_URI.unicode_string())
    yield
    await session_manager.close()


app = FastAPI(title=get_app_settings().APP_NAME, lifespan=lifespan)

register_exception_handlers(app)
app.include_router(category_router)
app.include_router(expense_router)


async def run_app():
    config = Config(
        app="expense_control.main:app",
        host=get_app_settings().APP_IP,
        port=get_app_settings().APP_PORT,
        reload=True,
        proxy_headers=True,
    )
    server = Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_app())
