from pydantic import BaseModel
from datetime import datetime

from expense_control.base.schemas import ConditionsFloat, BaseFilter


class ExpenseBase(BaseModel):
    type: bool
    category_id: int
    amount: float
    timestamp: datetime


class ExpenseUpdate(ExpenseBase):
    type: bool | None = None
    category_id: int | None = None
    amount: float | None = None
    timestamp: datetime | None = None


class ExpenseCreate(ExpenseBase):
    ...


class ExpenseSchema(ExpenseBase):
    id: int

    class Config:
        from_attributes = True


class ExpenseItem(BaseModel):
    id: int
    type: bool
    category_id: int
    category: str
    amount: float
    timestamp: datetime


class ExpenseFilter(BaseFilter):
    id: int | None = None
    type: bool | None = None
    category: str | None = None
    category_id: int | None = None
    amount: ConditionsFloat | None = None
    days: int | None = None
