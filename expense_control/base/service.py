from typing import TypeVar, Generic, Optional, Type, Sequence, Any

from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from sqlalchemy import select, ScalarResult, Row, RowMapping, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from expense_control.base.model import Base

Model = TypeVar('Model', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseService(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], database_session: AsyncSession):
        self.model = model
        self.database_session = database_session

    async def get_by_id(self, item_id: int) -> Optional[Model]:
        obj: Optional[Model] = await self.database_session.get(self.model, item_id)
        if obj is None:
            raise HTTPException(status_code=404, detail='Not found')
        return obj

    async def get_all(self) -> Optional[list[Model]]:
        query = select(self.model)
        objs = await self.database_session.execute(query)
        if not (objs := objs.scalars().all()):
            raise HTTPException(status_code=404, detail='Not found')
        return [obj for obj in objs]

    async def create(self, item_body: CreateSchema) -> Model:
        obj = self.model(**item_body.model_dump())

        self.database_session.add(obj)
        try:
            await self.database_session.commit()
        except IntegrityError as e:
            await self.database_session.rollback()
            if "UniqueViolationError" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        await self.database_session.refresh(obj)

        return obj
