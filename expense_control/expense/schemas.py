from pydantic import BaseModel
from datetime import datetime


class ExpenseBase(BaseModel):
    type: bool
    category_id: int


class ExpenseUpdate(ExpenseBase):
    ...


class ExpenseCreate(ExpenseBase):
    amount: float
    timestamp: datetime


class ExpenseSchema(ExpenseBase):
    id: int
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True
