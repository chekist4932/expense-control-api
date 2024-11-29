from fastapi import Depends

from typing import override, Type

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
                 condition_builder: ExpenseConditionBuilder,
                 mapper: ExpenseMapper | None):
        super().__init__(repository, condition_builder, mapper)

    @override
    async def get_all(self, filters: ExpenseFilter = None,
                      limit: int = 100,
                      offset: int = 0
                      ) -> list[ExpenseItem]:
        conditions = await self.condition_builder.build_condition(filters) if filters else []
        result_objs = await self.repository.get_all(conditions, limit, offset)
        return self.mapper.to_schemas(result_objs)


class GetExpenseService:
    """Get ExpenseService object with entity schema we needed"""

    def __init__(self, entity_schema: Type[ExpenseSchema | ExpenseItem] = None) -> None:
        self.entity_schema = entity_schema

    def __call__(self,
                 repository: ExpenseRepository = Depends(get_repository),
                 condition_builder: ExpenseConditionBuilder = Depends(get_condition_builder)
                 ) -> ExpenseService:
        if self.entity_schema:
            return ExpenseService(repository, condition_builder, ExpenseMapper(self.entity_schema))
        return ExpenseService(repository, condition_builder, None)
