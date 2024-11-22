from typing import Optional

from fastapi import APIRouter, Depends

from expense_control.category.service import CategoryService, get_category_service

from expense_control.category.schemas import (
    CategorySchema,
    CategoryCreate,
    CategoryUpdate)

category_router = APIRouter(prefix='/category', tags=['category'])


@category_router.get('/{category_id}', response_model=CategorySchema)
async def get_category_by_id(
        category_id: int, category_servie: CategoryService = Depends(get_category_service)
) -> Optional[CategorySchema]:
    return await category_servie.get_by_id(category_id)


@category_router.get('/', response_model=list[CategorySchema])
async def get_category_all(category_servie: CategoryService = Depends(get_category_service)
                           ) -> Optional[list[CategorySchema]]:
    return await category_servie.get_all()


@category_router.post('/', response_model=CategorySchema)
async def create_category(category: CategoryCreate, category_servie: CategoryService = Depends(get_category_service)
                          ) -> Optional[CategorySchema]:
    return await category_servie.create(category)


@category_router.patch('/{category_id}', response_model=CategorySchema)
async def update_category(category_id: int, category: CategoryUpdate,
                          category_servie: CategoryService = Depends(get_category_service)
                          ) -> Optional[CategorySchema]:
    return await category_servie.update(category_id, category)


@category_router.put('/{category_id}', response_model=CategorySchema)
async def update_category_full(category_id: int, category: CategoryCreate,
                               category_servie: CategoryService = Depends(get_category_service)
                               ) -> Optional[CategorySchema]:
    return await category_servie.update(category_id, category)


@category_router.delete('/{category_id}', status_code=204)
async def delete_category(category_id: int,
                          category_service: CategoryService = Depends(get_category_service)) -> None:
    return await category_service.delete(category_id)
