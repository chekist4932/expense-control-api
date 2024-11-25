from typing import Optional

from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import datetime

from expense_control.base.schemas import BaseFilter


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


class ExpenseItem(BaseModel):
    id: int
    type: bool
    category_id: int
    category: str
    amount: float
    timestamp: datetime


class ExpenseFilter(BaseFilter):
    id: Optional[int] = None
    type: Optional[bool] = None
    category: Optional[str] = None
    category_id: Optional[int] = None
    amount: Optional[dict[str, float]] = None
    days: Optional[int] = None

    @field_validator('amount', mode='before')
    @classmethod
    def validate_amount_operand(cls, field_value: str, values: ValidationInfo) -> dict[str, float]:
        return cls.validate_operand_field(field_value)
