from expense_control.base.filters import ConditionsFloat, BaseFilter


class ExpenseFilter(BaseFilter):
    id: int | None = None
    type: bool | None = None
    category: str | None = None
    category_id: int | None = None
    amount: ConditionsFloat | None = None
    days: int | None = None
