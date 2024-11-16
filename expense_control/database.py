from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import get_db_settings

engine = create_async_engine(get_db_settings().database_url, echo=False)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session
