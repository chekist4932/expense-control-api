from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.category.model import Category
from expense_control.category.schemas import CategoryCreate, CategoryUpdate, CategorySchema, CategoryFilter
from expense_control.category.repository import CategoryRepository, get_repository
from expense_control.category.mapper import CategoryMapper
from expense_control.category.condition import CategoryConditionBuilder, get_condition_builder


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

    def __call__(self,
                 repository: CategoryRepository = Depends(get_repository),
                 condition_builder: CategoryConditionBuilder = Depends(get_condition_builder)
                 ) -> CategoryService:

        mapper = CategoryMapper(self.entity_schema)  # Передается неявно. И что делать, когда схема None
        return CategoryService(repository, mapper, condition_builder)
