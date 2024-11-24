from typing import (TypeVar,
                    Generic,
                    Optional,
                    Type)

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from expense_control.base.model import Base

Model = TypeVar('Model', bound=Base)

CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)

EntitySchema = TypeVar('EntitySchema', bound=BaseModel)

FilterSchema = TypeVar('FilterSchema', bound=BaseModel)


class BaseService(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], entity_schema: Type[EntitySchema], database_session: AsyncSession):
        self.model = model
        self.database_session = database_session
        self.entity_schema = entity_schema

    async def get_by_id(self, obj_id: int, type_ret: bool = True) -> EntitySchema | Model:
        table_obj: Optional[Model] = await self.database_session.get(self.model, obj_id)

        if not table_obj:
            raise NoResultFound
        return self.entity_schema.from_orm(table_obj) if type_ret else table_obj

    async def get_all(self) -> Optional[list[EntitySchema]]:
        query = select(self.model)
        result_objs = await self.database_session.execute(query)

        if not (result_objs := result_objs.scalars().all()):
            raise NoResultFound

        return [self.entity_schema.from_orm(res_obj) for res_obj in result_objs]

    async def create(self, obj: CreateSchema) -> EntitySchema:
        table_obj = self.model(**obj.model_dump())
        self.database_session.add(table_obj)

        await self.database_session.commit()
        await self.database_session.refresh(table_obj)

        return self.entity_schema.from_orm(table_obj)

    async def update(self, obj_id: int, obj: UpdateSchema | CreateSchema) -> None:
        table_obj = await self.get_by_id(obj_id, type_ret=False)
        for key, value in obj.dict(exclude_none=True).items():
            setattr(table_obj, key, value)

        await self.database_session.commit()
        await self.database_session.refresh(table_obj)

    async def delete(self, obj_id: int) -> None:
        table_obj = await self.get_by_id(obj_id, type_ret=False)

        await self.database_session.delete(table_obj)
        await self.database_session.commit()
