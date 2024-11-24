from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from typing import override

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseCreate, ExpenseUpdate, ExpenseSchema, ExpenseItem

from expense_control.category.model import Category


class ExpenseService(BaseService[Expense, ExpenseCreate, ExpenseUpdate]):
    def __init__(self, database_session: AsyncSession):
        super().__init__(Expense, ExpenseSchema, database_session)

    @override
    async def get_by_id(self, obj_id: int, type_ret: bool = True) -> ExpenseItem | Expense:
        if not type_ret:
            return await super().get_by_id(obj_id, False)

        query = select(self.model.id,
                       self.model.type,
                       self.model.amount,
                       self.model.timestamp,
                       self.model.category_id,
                       Category.name.label('category')).join(Category).where(self.model.id == obj_id)

        result_obj = await self.database_session.execute(query)

        if not (result_obj := result_obj.mappings().first()):
            raise NoResultFound

        return ExpenseItem(**result_obj)


def get_expense_service(database_session: AsyncSession = Depends(get_async_session)):
    return ExpenseService(database_session)
