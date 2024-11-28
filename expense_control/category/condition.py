from expense_control.base import ConditionBuilder

from expense_control.category.model import Category


class CategoryConditionBuilder(ConditionBuilder[Category]):
    def __init__(self):
        super().__init__(Category)


# condition_builder = CategoryConditionBuilder()


async def get_condition_builder():
    return CategoryConditionBuilder()
