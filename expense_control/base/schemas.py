from json import loads
from types import UnionType
from typing import get_origin, Union, get_args, Any, Generic

from pydantic import BaseModel, field_validator, Field

from expense_control.base.types import EntitySchema


class Conditions(BaseModel):
    @classmethod
    def validate_operand_field(cls, field_value: str):
        field = loads(field_value)
        return cls(**field)


class ConditionsInt(Conditions):
    gt: int | None = None
    lt: int | None


class ConditionsFloat(Conditions):
    gt: float | None = None
    lt: float | None


class BaseFilter(BaseModel):
    @field_validator('*', mode='before')
    @classmethod
    def validate_conditions_fields(cls, field_value, info) -> Conditions | Any:
        """
        Validation field with type Conditions or its subclasses.
        """
        field_type = cls.model_fields[info.field_name].annotation
        origin_annotation = get_origin(field_type)

        if origin_annotation is Union or origin_annotation is UnionType:
            field_type = next((arg for arg in get_args(field_type) if issubclass(arg, Conditions)), None)

        if field_type:
            return field_type.validate_operand_field(field_value)

        return field_value


class PaginatedResponse(BaseModel, Generic[EntitySchema]):
    count: int = Field(description='Number of items returned in the response')
    items: list[EntitySchema] = Field(description='List of items returned in the response following given criteria')
