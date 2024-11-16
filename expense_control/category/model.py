from sqlalchemy import Column, Integer, UniqueConstraint, String

from expense_control.base import Base


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (UniqueConstraint('name'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
