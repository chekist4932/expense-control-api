from expense_control.base import ConditionBuilder

from expense_control.category.model import Category


class CategoryConditionBuilder(ConditionBuilder[Category]):
    def __init__(self, model):
        super().__init__(model)
