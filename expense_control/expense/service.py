from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.database import get_async_session

from expense_control.base import BaseService
from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseCreate, ExpenseUpdate


class ExpenseService(BaseService[Expense, ExpenseCreate, ExpenseUpdate]):
    def __init__(self, database_session: AsyncSession):
        super(ExpenseService, self).__init__(Expense, database_session)


def get_expense_service(database_session: AsyncSession = Depends(get_async_session)):
    return ExpenseService(database_session)
