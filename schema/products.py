from pydantic import BaseModel,ConfigDict
from typing import Optional, List

from schema.categories import CategoryResponse

class ProductBase(BaseModel):
    name: str
    price: int
    stock: int


class ProductCreate(ProductBase):
    category_ids: List[int] =[]

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    name: str
    price: int
    categories: List[CategoryResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ProductFiltering(BaseModel):
    name: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    category_id: Optional[int] = None