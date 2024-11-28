from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.base import BaseRepository
from expense_control.category.model import Category

from expense_control.database import get_async_session


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)


async def get_repository(session: AsyncSession = Depends(get_async_session)) -> CategoryRepository:
    return CategoryRepository(session)
