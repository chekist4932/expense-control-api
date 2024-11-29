from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
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
                 condition_builder: CategoryConditionBuilder,
                 mapper: CategoryMapper | None):
        super().__init__(repository, condition_builder, mapper)


class GetCategoryService:
    """Get CategoryService object with entity schema we needed"""

    def __init__(self, entity_schema: Type[CategorySchema] | None = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self,
                 repository: CategoryRepository = Depends(get_repository),
                 condition_builder: CategoryConditionBuilder = Depends(get_condition_builder)
                 ) -> CategoryService:
        if self.entity_schema:
            return CategoryService(repository, condition_builder, CategoryMapper(self.entity_schema))
        return CategoryService(repository, condition_builder, None)
