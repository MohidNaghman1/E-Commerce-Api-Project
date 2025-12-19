
from pydantic import BaseModel,ConfigDict
from typing import List,Optional
from schema.order_item import OrderItemResponse, OrderItemCreate
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"


class OrderBase(BaseModel):
    status: OrderStatus

class OrderCreate(OrderBase):
    user_id: int
    items: Optional[List[OrderItemCreate]] = []

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderResponse(OrderBase):
    id: int
    user_id: int
    total: int
    order_items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)