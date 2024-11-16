from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryUpdate(CategoryBase):
    ...


class CategoryCreate(CategoryBase):
    ...


class CategorySchema(CategoryBase):
    id: int

    class Config:
        from_attributes = True
