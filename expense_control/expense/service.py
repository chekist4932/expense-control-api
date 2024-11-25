from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from typing import override, Optional, Union

from expense_control.base.service import EntitySchema
from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseCreate, ExpenseUpdate, ExpenseItem, ExpenseSchema

from expense_control.category.model import Category


class ExpenseService(BaseService[Expense, ExpenseCreate, ExpenseUpdate]):
    def __init__(self, entity_schema: Optional[ExpenseSchema or ExpenseItem], database_session: AsyncSession):
        super().__init__(Expense, entity_schema, database_session)

    @override
    async def get_all(self) -> list[ExpenseItem]:
        query = select(self.model.id,
                       self.model.type,
                       self.model.amount,
                       self.model.timestamp,
                       self.model.category_id,
                       Category.name.label('category')).join(Category)

        result_objs = await self.database_session.execute(query)

        if not (result_objs := result_objs.mappings().all()):
            raise NoResultFound

        return [self.entity_schema(**res_obj) for res_obj in result_objs]


class GetExpenseService:
    """Get ExpenseService object with entity schema we needed"""

    def __init__(self, entity_schema: Optional[ExpenseSchema or ExpenseItem] = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self, database_session: AsyncSession = Depends(get_async_session)) -> ExpenseService:
        return ExpenseService(self.entity_schema, database_session)
