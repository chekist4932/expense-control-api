from typing import Generic, Type
from sqlalchemy import Row, RowMapping

from expense_control.base.types import EntitySchema, Model


class EntityMapper(Generic[Model, EntitySchema]):
    def __init__(self, entity_schema: Type[EntitySchema]):
        self.entity_schema = entity_schema

    def to_schema(self, entity: Model | Row | RowMapping) -> EntitySchema:
        return self.entity_schema.from_orm(entity)

    def to_schemas(self, entities: Model) -> list[EntitySchema]:
        return [self.entity_schema.from_orm(entity) for entity in entities]
