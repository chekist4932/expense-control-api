from expense_control.base.filters import BaseFilter, ConditionsInt


class CategoryFilter(BaseFilter):
    name: str | None = None
    rate: ConditionsInt | None = None
