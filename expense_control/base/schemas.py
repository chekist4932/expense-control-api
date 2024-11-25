from json import loads

from pydantic import BaseModel


class BaseFilter(BaseModel):
    @staticmethod
    def validate_operand_field(field_value: str) -> dict[str, float] or dict[str, int]:
        field = loads(field_value)
        allowed_keys = {'lt', 'gt'}

        if not all(key in allowed_keys for key in field):
            raise ValueError('Not allowed key')

        if len(field) == len(allowed_keys) and field['gt'] > field['lt']:
            raise ValueError('gt > lt')

        return field
