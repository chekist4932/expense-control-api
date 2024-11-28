from typing import Generic, Type
from sqlalchemy import RowMapping, Row

from expense_control.base.types import EntitySchema, Model


class EntityMapper(Generic[Model, EntitySchema]):
    def __init__(self, entity_schema: Type[EntitySchema]):
        self.entity_schema = entity_schema

    def to_schema(self, entity: Model | RowMapping) -> EntitySchema:
        if isinstance(entity, RowMapping):
            return self.entity_schema(**entity)
        return self.entity_schema.from_orm(entity)

    def to_schemas(self, entities: Model | RowMapping) -> list[EntitySchema]:
        return [self.to_schema(entity) for entity in entities]
