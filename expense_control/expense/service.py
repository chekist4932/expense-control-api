from fastapi import Depends

from typing import override

from expense_control.base import BaseService
from expense_control.expense.model import Expense
from expense_control.expense.schemas import (
    ExpenseCreate, ExpenseUpdate, ExpenseItem, ExpenseSchema)

from expense_control.expense.schemas import ExpenseFilter
from expense_control.expense.repository import ExpenseRepository, get_repository
from expense_control.expense.mapper import ExpenseMapper
from expense_control.expense.condition import ExpenseConditionBuilder, get_condition_builder


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

    def __call__(self,
                 repository: ExpenseRepository = Depends(get_repository),
                 condition_builder: ExpenseConditionBuilder = Depends(get_condition_builder)
                 ) -> ExpenseService:
        mapper = ExpenseMapper(self.entity_schema)  # Передается неявно. И что делать, когда схема None
        return ExpenseService(repository, mapper, condition_builder)
