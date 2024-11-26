from pydantic import BaseModel
from datetime import datetime


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
