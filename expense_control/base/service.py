from typing import TypeVar, Generic, Optional, Type, Sequence, Any

from pydantic import BaseModel

from sqlalchemy import select, ScalarResult, Row, RowMapping, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DatabaseError, NoResultFound

from expense_control.base.model import Base

Model = TypeVar('Model', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
FilterSchema = TypeVar('FilterSchema', bound=BaseModel)


class BaseService(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], database_session: AsyncSession):
        self.model = model
        self.database_session = database_session

    async def get_by_id(self, obj_id: int) -> Optional[Model]:
        db_obj: Optional[Model] = await self.database_session.get(self.model, obj_id)

        if not db_obj:
            raise NoResultFound

        return db_obj

    async def get_all(self) -> Optional[list[Model]]:
        query = select(self.model)
        db_objs = await self.database_session.execute(query)

        if not (db_objs := db_objs.scalars().all()):
            raise NoResultFound

        return [db_obj for db_obj in db_objs]

    async def create(self, obj: CreateSchema) -> Model:
        db_obj = self.model(**obj.model_dump())
        self.database_session.add(db_obj)

        await self.database_session.commit()
        await self.database_session.refresh(db_obj)

        return db_obj

    async def update(self, obj_id: int, obj: UpdateSchema | CreateSchema) -> Model:
        db_obj: Model = await self.database_session.get(self.model, obj_id)

        if not db_obj:
            raise NoResultFound

        for key, value in obj.dict(exclude_none=True).items():
            setattr(db_obj, key, value)

        await self.database_session.commit()
        await self.database_session.refresh(db_obj)

        return db_obj

    async def delete(self, obj_id: int) -> None:
        db_obj = await self.database_session.get(self.model, obj_id)

        if not db_obj:
            raise NoResultFound

        await self.database_session.delete(db_obj)
        await self.database_session.commit()
