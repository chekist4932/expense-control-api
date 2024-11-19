from sqlalchemy import Column, Integer, UniqueConstraint, String, CheckConstraint

from expense_control.base import Base


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (UniqueConstraint('name'),
                      CheckConstraint("rate > 0 AND rate < 11",
                                      name="chk_rate"),
                      )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
