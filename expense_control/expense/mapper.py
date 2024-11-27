from typing import override
from sqlalchemy import Row, RowMapping
from expense_control.base import EntityMapper

from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseItem, ExpenseSchema


class ExpenseMapper(EntityMapper[Expense, ExpenseItem | ExpenseSchema]):
    def __init__(self, entity_schema):
        super().__init__(entity_schema)

    @override
    def to_schemas(self, entities: Row | RowMapping) -> list[ExpenseItem]:
        return [self.entity_schema(**entity) for entity in entities]
