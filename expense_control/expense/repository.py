from typing import Any, override
from fastapi import Depends
from sqlalchemy import BinaryExpression, Row, RowMapping, select, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.base import BaseRepository
from expense_control.expense.model import Expense
from expense_control.category.model import Category
from expense_control.database import get_async_session


class ExpenseRepository(BaseRepository[Expense]):

    def __init__(self, session: AsyncSession):
        super().__init__(Expense, session)

    @override
    async def get_all(self, conditions: list[BinaryExpression] | None = None,
                      limit: int = 100,
                      offset: int = 0
                      ) -> Row[Any] | RowMapping | Any:
        query = (
            select(self.model.id,
                   self.model.type,
                   self.model.amount,
                   self.model.timestamp,
                   self.model.category_id,
                   Category.name.label('category'))  # Передается неявно
            .join(Category).limit(limit).offset(offset).order_by(self.model.id)
        )

        if conditions:
            query = query.where(and_(*conditions))

        result_objs = await self.session.execute(query)
        if not (result_objs := result_objs.mappings().all()):
            raise NoResultFound

        return result_objs


async def get_repository(session: AsyncSession = Depends(get_async_session)) -> ExpenseRepository:
    return ExpenseRepository(session)
