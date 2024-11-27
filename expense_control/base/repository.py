from typing import Any, Generic, Type
from sqlalchemy import and_, BinaryExpression, select, Row, RowMapping
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.base.types import FilterSchema, Model


class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, obj_id: int) -> Model:
        obj = await self.session.get(self.model, obj_id)
        if not obj:
            raise NoResultFound
        return obj

    async def get_all(self, conditions: list[BinaryExpression] | None = None) -> Row[Any] | RowMapping | Any:
        query = select(self.model)

        if conditions:
            query = query.filter(and_(*conditions))
        result_objs = await self.session.execute(query)
        if not (result_objs := result_objs.scalars().all()):
            raise NoResultFound

        return result_objs

    async def add(self, obj: Model) -> None:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

    async def delete(self, obj: Model) -> None:
        await self.session.delete(obj)
        await self.session.commit()
