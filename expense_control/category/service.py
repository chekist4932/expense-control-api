from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.category.model import Category
from expense_control.category.schemas import CategoryCreate, CategoryUpdate, CategorySchema


class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self, entity_schema: CategorySchema or None, database_session: AsyncSession):
        super().__init__(Category, entity_schema, database_session)


# def get_category_service(database_session: AsyncSession = Depends(get_async_session)):
#     return CategoryService(database_session)

class GetCategoryService:
    """Get CategoryService object with entity schema we needed"""

    def __init__(self, entity_schema: CategorySchema or None = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self, database_session: AsyncSession = Depends(get_async_session)) -> CategoryService:
        return CategoryService(self.entity_schema, database_session)
