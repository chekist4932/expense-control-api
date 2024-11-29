from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, Query

from expense_control.category.service import CategoryService, GetCategoryService

from expense_control.category.schemas import (
    CategorySchema,
    CategoryCreate,
    CategoryUpdate,
    CategoryFilter
)

from expense_control.base.schemas import PaginatedResponse

category_router = APIRouter(prefix='/category', tags=['category'])


@category_router.get('/{category_id}', response_model=CategorySchema)
async def get_category_by_id(
        category_id: int, category_servie: CategoryService = Depends(GetCategoryService(CategorySchema))
) -> CategorySchema:
    return await category_servie.get_by_id(category_id)


@category_router.get('/', response_model=PaginatedResponse[CategorySchema])
async def get_category_all(filters: Annotated[CategoryFilter, Query()] = None,
                           category_servie: CategoryService = Depends(GetCategoryService(CategorySchema)),
                           limit: int = Query(100, ge=0),
                           offset: int = Query(0, ge=0)
                           ) -> dict[str, int | list[CategorySchema] | None]:
    items = await category_servie.get_all(filters, limit, offset)
    return {
        'count': len(items),
        'items': items
    }


@category_router.post('/', response_model=CategorySchema)
async def create_category(category: CategoryCreate,
                          category_servie: CategoryService = Depends(GetCategoryService(CategorySchema))
                          ) -> CategorySchema:
    return await category_servie.create(category)


@category_router.patch('/{category_id}', status_code=204)
async def update_category(category_id: int, category: CategoryUpdate,
                          category_servie: CategoryService = Depends(GetCategoryService())
                          ) -> None:
    return await category_servie.update(category_id, category)


@category_router.put('/{category_id}', status_code=204)
async def update_category_full(category_id: int, category: CategoryCreate,
                               category_servie: CategoryService = Depends(GetCategoryService())
                               ) -> None:
    return await category_servie.update(category_id, category)


@category_router.delete('/{category_id}', status_code=204)
async def delete_category(category_id: int,
                          category_service: CategoryService = Depends(GetCategoryService())
                          ) -> None:
    return await category_service.delete(category_id)
