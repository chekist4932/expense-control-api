from typing import Optional

from fastapi import APIRouter, Depends

from expense_control.category.service import CategoryService, get_category_service
from expense_control.category.model import Category
from expense_control.category.schemas import CategorySchema

category_router = APIRouter(prefix='/category', tags=['category'])


@category_router.get('/{id}', response_model=CategorySchema)
async def get_category_by_id(
        category_id: int, category_servie: CategoryService = Depends(get_category_service)
) -> Optional[Category]:
    return await category_servie.get_by_id(category_id)


@category_router.get('/', response_model=list[CategorySchema])
async def get_category_all(category_servie: CategoryService = Depends(get_category_service)
                           ) -> Optional[list[Category]]:
    return await category_servie.get_all()
