from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, Query

from expense_control.expense.service import ExpenseService, GetExpenseService
from expense_control.expense.schemas import (
    ExpenseSchema,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseItem,
    ExpenseFilter
)
from expense_control.base.schemas import PaginatedResponse

expense_router = APIRouter(prefix='/expense', tags=['expense'])


@expense_router.get('/{expense_id}', response_model=ExpenseSchema)
async def get_expense_by_id(
        expense_id: int, expense_servie: ExpenseService = Depends(GetExpenseService(ExpenseSchema))
) -> ExpenseItem:
    return await expense_servie.get_by_id(expense_id)


@expense_router.get('/', response_model=PaginatedResponse[ExpenseItem])
async def get_expense_all(filters: Annotated[ExpenseFilter, Query()] = None,
                          expense_servie: ExpenseService = Depends(GetExpenseService(ExpenseItem)),
                          limit: int = Query(100, ge=0),
                          offset: int = Query(0, ge=0)
                          ) -> dict[str, int | list[ExpenseItem]]:
    items = await expense_servie.get_all(filters, limit, offset)
    return {
        'count': len(items),
        'items': items
    }


@expense_router.post('/', response_model=ExpenseSchema)
async def create_expense(expense: ExpenseCreate,
                         expense_servie: ExpenseService = Depends(GetExpenseService(ExpenseSchema))
                         ) -> ExpenseSchema:
    return await expense_servie.create(expense)


@expense_router.patch('/{expense_id}', status_code=204)
async def update_expense(expense_id: int, expense: ExpenseUpdate,
                         expense_servie: ExpenseService = Depends(GetExpenseService())
                         ) -> None:
    return await expense_servie.update(expense_id, expense)


@expense_router.put('/{expense_id}', status_code=201)
async def update_expense_full(expense_id: int, expense: ExpenseCreate,
                              expense_servie: ExpenseService = Depends(GetExpenseService())
                              ) -> None:
    return await expense_servie.update(expense_id, expense)


@expense_router.delete('/{expense_id}', status_code=204)
async def delete_expense(expense_id: int,
                         expense_servie: ExpenseService = Depends(GetExpenseService())
                         ) -> None:
    return await expense_servie.delete(expense_id)
