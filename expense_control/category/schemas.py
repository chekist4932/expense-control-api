from typing import Optional
from pydantic import BaseModel, field_validator, ValidationInfo

from expense_control.base.schemas import BaseFilter


class CategoryBase(BaseModel):
    name: str
    rate: int = 1

    @field_validator('rate', mode='after')
    @classmethod
    def validate_rate(cls, field_value: int, values: ValidationInfo) -> int:
        if not (1 <= field_value <= 10):  # Проверяем диапазон 1–10
            raise ValueError("The 'rate' must be between 1 and 10 inclusive")

        return field_value


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    rate: Optional[int] = None


class CategoryCreate(CategoryBase):
    ...


class CategorySchema(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryFilter(BaseFilter):
    name: Optional[str] = None
    rate: Optional[dict[str, int]] = None

    @field_validator('rate', mode='before')
    @classmethod
    def validate_rate_operand(cls, field_value: str, values: ValidationInfo) -> dict[str, int]:
        return cls.validate_operand_field(field_value)
