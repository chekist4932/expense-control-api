from typing import Any, override

from sqlalchemy import BinaryExpression, Row, RowMapping, select, and_
from sqlalchemy.exc import NoResultFound

from expense_control.base import BaseRepository
from expense_control.expense.model import Expense
from expense_control.category.model import Category


class ExpenseRepository(BaseRepository[Expense]):

    @override
    async def get_all(self, conditions: list[BinaryExpression] | None = None) -> Row[Any] | RowMapping | Any:
        query = (
            select(self.model.id,
                   self.model.type,
                   self.model.amount,
                   self.model.timestamp,
                   self.model.category_id,
                   Category.name.label('category'))  # Передается неявно
            .join(Category)
        )

        if conditions:
            query = query.where(and_(*conditions))

        result_objs = await self.session.execute(query)
        if not (result_objs := result_objs.mappings().all()):
            raise NoResultFound

        return result_objs
