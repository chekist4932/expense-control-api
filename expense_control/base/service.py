from typing import Generic

from expense_control.base.types import Model, CreateSchema, UpdateSchema, EntitySchema, FilterSchema
from expense_control.base.repository import BaseRepository
from expense_control.base.mapper import EntityMapper
from expense_control.base.condition import ConditionBuilder


class BaseService(Generic[Model, CreateSchema, UpdateSchema, EntitySchema, FilterSchema]):
    def __init__(
            self,
            repository: BaseRepository[Model],
            mapper: EntityMapper[Model, EntitySchema],
            condition_builder: ConditionBuilder[Model]
    ):
        self.repository = repository
        self.mapper = mapper
        self.condition_builder = condition_builder

    async def get_by_id(self, obj_id: int) -> EntitySchema:
        entity = await self.repository.get_by_id(obj_id)
        return self.mapper.to_schema(entity)

    async def get_all(self, filters: FilterSchema | None = None) -> list[EntitySchema] | None:
        conditions = await self.condition_builder.build_condition(filters) if filters else []
        result_objs = await self.repository.get_all(conditions)
        return self.mapper.to_schemas(result_objs)

    async def create(self, obj: CreateSchema) -> EntitySchema:
        entity = self.repository.model(**obj.model_dump())
        await self.repository.add(entity)
        return self.mapper.to_schema(entity)

    async def update(self, obj_id: int, obj: UpdateSchema | CreateSchema) -> None:
        entity = await self.repository.get_by_id(obj_id)
        for key, value in obj.model_dump(exclude_none=True).items():
            setattr(entity, key, value)
        await self.repository.add(entity)

    async def delete(self, obj_id: int) -> None:
        entity = await self.repository.get_by_id(obj_id)
        await self.repository.delete(entity)
