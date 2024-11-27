from typing import Generic, Type
from sqlalchemy import BinaryExpression
from expense_control.base.types import FilterSchema, Model


class ConditionBuilder(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model

    async def build_condition(self, filters: FilterSchema) -> list[BinaryExpression] | list:
        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if isinstance(value, dict):
                column = getattr(self.model, field)
                for operand, val in value.items():
                    if operand == 'gt':
                        conditions.append(column > val)
                    elif operand == 'lt':
                        conditions.append(column < val)
            elif hasattr(self.model, field):
                column = getattr(self.model, field)
                conditions.append(column == value)
        return conditions
