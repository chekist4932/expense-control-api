from typing import Optional

from fastapi import APIRouter, Depends

from expense_control.expense.service import ExpenseService, get_expense_service
from expense_control.expense.model import Expense
from expense_control.expense.schemas import ExpenseSchema

expense_router = APIRouter(prefix='/expense', tags=['expense'])


@expense_router.get('/{id}', response_model=ExpenseSchema)
async def get_expense_by_id(
        category_id: int, expense_servie: ExpenseService = Depends(get_expense_service)
) -> Optional[Expense]:
    return await expense_servie.get_by_id(category_id)


@expense_router.get('/', response_model=list[ExpenseSchema])
async def get_expense_all(expense_servie: ExpenseService = Depends(get_expense_service)
                          ) -> Optional[list[Expense]]:
    return await expense_servie.get_all()
