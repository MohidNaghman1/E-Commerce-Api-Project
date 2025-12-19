from pydantic import BaseModel,ConfigDict
from typing import List,Optional


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    order_id: Optional[int] = None

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None

class OrderItemResponse(OrderItemBase):
    id: int
    price: int

    model_config = ConfigDict(from_attributes=True)