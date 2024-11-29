from expense_control.base import EntityMapper
from expense_control.category.model import Category
from expense_control.category.schemas import CategorySchema


class CategoryMapper(EntityMapper[Category, CategorySchema]):
    def __init__(self, entity_schema):
        super().__init__(entity_schema)
