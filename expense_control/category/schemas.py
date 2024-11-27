from pydantic import BaseModel, field_validator, ValidationInfo

from expense_control.base.schemas import BaseFilter, ConditionsInt


class CategoryBase(BaseModel):
    name: str
    rate: int = 1

    @field_validator('rate', mode='after')
    @classmethod
    def validate_rate(cls, field_value: int, values: ValidationInfo) -> int:
        if not (1 <= field_value <= 10):
            raise ValueError("Rate must be >= 1 and <= 10")

        return field_value


class CategoryUpdate(CategoryBase):
    name: str | None = None
    rate: int | None = None


class CategoryCreate(CategoryBase):
    ...


class CategorySchema(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryFilter(BaseFilter):
    name: str | None = None
    rate: ConditionsInt | None = None
