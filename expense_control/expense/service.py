from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from typing import override

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.expense.model import Expense
from expense_control.expense.schemas import (
    ExpenseCreate, ExpenseUpdate, ExpenseItem, ExpenseSchema)

from expense_control.expense.schemas import ExpenseFilter
from expense_control.expense.repository import ExpenseRepository
from expense_control.expense.mapper import ExpenseMapper
from expense_control.expense.condition import ExpenseConditionBuilder


class ExpenseService(BaseService[Expense, ExpenseCreate, ExpenseUpdate, ExpenseItem | ExpenseSchema, ExpenseFilter]):
    def __init__(self,
                 repository: ExpenseRepository,
                 mapper: ExpenseMapper,
                 condition_builder: ExpenseConditionBuilder):
        super().__init__(repository, mapper, condition_builder)

    @override
    async def get_all(self, filters: ExpenseFilter = None) -> list[ExpenseItem]:
        conditions = await self.condition_builder.build_condition(filters) if filters else []
        result_objs = await self.repository.get_all(conditions)
        return self.mapper.to_schemas(result_objs)


class GetExpenseService:
    """Get ExpenseService object with entity schema we needed"""

    def __init__(self, entity_schema: ExpenseSchema | ExpenseItem = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self, session: AsyncSession = Depends(get_async_session)) -> ExpenseService:
        repository = ExpenseRepository(Expense, session)  # Передается неявно
        mapper = ExpenseMapper(self.entity_schema)  # Передается неявно. И что делать, когда схема None
        condition_builder = ExpenseConditionBuilder(Expense)  # Передается неявно
        return ExpenseService(repository, mapper, condition_builder)

# Мб создать файлы mapper.py, repository.py и move filters.py -> condition.py
