from typing import Any, Generic, Type
from functools import wraps
from sqlalchemy import and_, BinaryExpression, select, Row, RowMapping
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from expense_control.base.types import Model


class AttributeCheckerMeta(type):
    """
    Проверка, является ли session None.
    """

    def __new__(cls, name, bases, dct):
        for attr_name, value in dct.items():
            if callable(value) and not attr_name.startswith("__") and attr_name:
                dct[attr_name] = cls.wrap_method(value)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def wrap_method(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if getattr(self, "session", None) is None:
                raise ValueError(f"session can't be None before calling '{method.__name__}'")
            return method(self, *args, **kwargs)

        return wrapper


class BaseRepository(Generic[Model], metaclass=AttributeCheckerMeta):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @session.setter
    def session(self, session: AsyncSession):
        if not isinstance(session, AsyncSession):
            raise TypeError(f"Expected 'AsyncSession', got {type(session).__name__}")
        self._session = session

    async def get_by_id(self, obj_id: int) -> Model:
        obj = await self.session.get(self.model, obj_id)
        if not obj:
            raise NoResultFound
        return obj

    async def get_all(self, conditions: list[BinaryExpression] | None = None,
                      limit: int = 100,
                      offset: int = 0
                      ) -> Row[Any] | RowMapping | Any:
        query = select(self.model).limit(limit).offset(offset).order_by(self.model.id)

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
