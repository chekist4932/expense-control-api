from typing import TypeVar, Generic, Optional, Type, Callable, Sequence, Any
from functools import wraps

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from expense_control.base.model import Base

Model = TypeVar('Model', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
FilterSchema = TypeVar('FilterSchema', bound=BaseModel)


def inject_obj(method: Callable):
    @wraps(method)
    async def wrapper(self, obj_id: int, *args, **kwargs) -> Optional[Model]:
        db_obj: Optional[Model] = await self.database_session.get(self.model, obj_id)
        if not db_obj:
            raise NoResultFound
        return await method(self, db_obj, *args, **kwargs)

    return wrapper


class BaseService(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], database_session: AsyncSession):
        self.model = model
        self.database_session = database_session

    @inject_obj
    async def get_by_id(self, db_obj: Model) -> Optional[Model]:
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

    @inject_obj
    async def update(self, db_obj: Model, obj: UpdateSchema | CreateSchema) -> Model:
        for key, value in obj.dict(exclude_none=True).items():
            setattr(db_obj, key, value)

        await self.database_session.commit()
        await self.database_session.refresh(db_obj)

        return db_obj

    @inject_obj
    async def delete(self, db_obj: Model) -> None:
        await self.database_session.delete(db_obj)
        await self.database_session.commit()
