from typing import AsyncGenerator, Optional, AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine, AsyncConnection
from sqlalchemy.exc import SQLAlchemyError

from expense_control.base import Base


ERROR_MSG = "DatabaseSessionManager is not initialized"


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, database_url: str) -> None:
        self._engine = create_async_engine(database_url, echo=False, pool_pre_ping=True)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, class_=AsyncSession)

    async def close(self) -> None:
        if self._engine is None:
            raise SQLAlchemyError(ERROR_MSG)

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise SQLAlchemyError(ERROR_MSG)

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise SQLAlchemyError(ERROR_MSG)

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @staticmethod
    async def create_all_conn(connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_all_conn(connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


session_manager = DatabaseSessionManager()


async def get_async_session() -> AsyncGenerator:
    async with session_manager.session() as session:
        yield session
