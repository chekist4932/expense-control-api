from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.category.model import Category
from expense_control.category.schemas import CategoryCreate, CategoryUpdate, CategorySchema, CategoryFilter
from expense_control.category.repository import CategoryRepository
from expense_control.category.mapper import CategoryMapper
from expense_control.category.condition import CategoryConditionBuilder


class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate, CategorySchema, CategoryFilter]):
    def __init__(self,
                 repository: CategoryRepository,
                 mapper: CategoryMapper,
                 condition_builder: CategoryConditionBuilder):
        super().__init__(repository, mapper, condition_builder)


class GetCategoryService:
    """Get CategoryService object with entity schema we needed"""

    def __init__(self, entity_schema: CategorySchema | None = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self, session: AsyncSession = Depends(get_async_session)) -> CategoryService:
        repository = CategoryRepository(Category, session)  # Передается неявно
        mapper = CategoryMapper(self.entity_schema)  # Передается неявно. И что делать, когда схема None
        condition_builder = CategoryConditionBuilder(Category)  # Передается неявно
        return CategoryService(repository, mapper, condition_builder)
