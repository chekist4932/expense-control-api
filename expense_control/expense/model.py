from datetime import datetime, UTC

from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, UniqueConstraint, Boolean

from expense_control.base import Base


class Expense(Base):
    __tablename__ = 'expense'
    __table_args__ = (UniqueConstraint('timestamp', 'amount', 'type', 'category_id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Boolean, nullable=False)
    amount = Column(DECIMAL(precision=32, scale=2), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='RESTRICT'))
    timestamp = Column(DateTime, default=datetime.now(UTC))
