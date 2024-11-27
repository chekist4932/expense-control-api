from expense_control.base import BaseRepository
from expense_control.category.model import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, model, session):
        super().__init__(model, session)
