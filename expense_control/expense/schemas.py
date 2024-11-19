from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class ExpenseBase(BaseModel):
    type: bool
    category_id: int
    amount: float
    timestamp: datetime


class ExpenseUpdate(ExpenseBase):
    type: Optional[bool] = None
    category_id: Optional[int] = None
    amount: Optional[float] = None
    timestamp: Optional[datetime] = None


class ExpenseCreate(ExpenseBase):
    ...


class ExpenseSchema(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
