from pydantic import BaseModel,ConfigDict
from typing import Optional

class CartItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    quantity: int

class CartItemCreate(CartItemBase):
    user_id: int
    product_id: int

class CartItemUpdate(CartItemBase):
    quantity: Optional[int] = None


class CartItemResponse(CartItemBase):
    id: int
    user_id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)