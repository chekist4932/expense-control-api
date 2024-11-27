from datetime import timedelta
from typing import override

from sqlalchemy import func, BinaryExpression

from expense_control.base import ConditionBuilder
from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseFilter

from expense_control.category.model import Category


class ExpenseConditionBuilder(ConditionBuilder[Expense]):
    @override
    async def build_condition(self, filters: ExpenseFilter) -> list[BinaryExpression]:
        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == 'days':
                column = getattr(self.model, 'timestamp')
                conditions.append(column >= func.current_timestamp() - timedelta(days=value))
            elif field == 'category':
                column = getattr(Category, 'name')  # Refactor in future
                conditions.append(column == value)
            elif isinstance(value, dict):
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
