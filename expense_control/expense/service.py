from datetime import timedelta

from fastapi import Depends
from sqlalchemy import select, and_, BinaryExpression, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from typing import override, Optional

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.expense.model import Expense
from expense_control.expense.schemas import (
    ExpenseCreate, ExpenseUpdate, ExpenseItem, ExpenseSchema, ExpenseFilter)

from expense_control.category.model import Category


class ExpenseService(BaseService[Expense, ExpenseCreate, ExpenseUpdate]):
    def __init__(self, entity_schema: Optional[ExpenseSchema or ExpenseItem], database_session: AsyncSession):
        super().__init__(Expense, entity_schema, database_session)

    @override
    async def get_all(self, filters: ExpenseFilter or None = None) -> list[ExpenseItem]:

        query = select(self.model.id,
                       self.model.type,
                       self.model.amount,
                       self.model.timestamp,
                       self.model.category_id,
                       Category.name.label('category')).join(Category)

        if conditions := await self.get_conditions(filters):
            query = query.where(and_(*conditions))

        result_objs = await self.database_session.execute(query)

        if not (result_objs := result_objs.mappings().all()):
            raise NoResultFound

        return [self.entity_schema(**res_obj) for res_obj in result_objs]

    @override
    async def get_conditions(self, filters: ExpenseFilter) -> list[BinaryExpression] or list:
        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == 'days':
                column = getattr(self.model, 'timestamp')
                conditions.append(column >= func.current_timestamp() - timedelta(days=value))
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
            elif 'category' in field:
                column = getattr(Category, 'name')
                conditions.append(column == value)
        return conditions


class GetExpenseService:
    """Get ExpenseService object with entity schema we needed"""

    def __init__(self, entity_schema: Optional[ExpenseSchema or ExpenseItem] = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self, database_session: AsyncSession = Depends(get_async_session)) -> ExpenseService:
        return ExpenseService(self.entity_schema, database_session)
