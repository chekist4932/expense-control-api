from expense_control.base import EntityMapper

from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseItem, ExpenseSchema


class ExpenseMapper(EntityMapper[Expense, ExpenseItem | ExpenseSchema]):
    def __init__(self, entity_schema):
        super().__init__(entity_schema)
