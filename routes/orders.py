from fastapi import APIRouter, Depends, HTTPException
from services.order_service import OrderService
from services.orderitem_service import OrderItemService
from Repositories import OrderRepository,ProductRepository,UserRepository,OrderItemRepository,CategoryRepository
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schema import OrderCreate, OrderResponse,OrderUpdate


order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.post("/", response_model=OrderResponse)
async def create_order(order_create: OrderCreate, db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)
    user_repo = UserRepository(db)
    category_repo = CategoryRepository(db)
    order_item_repo = OrderItemRepository(db)
    order_service = OrderService(order_repo, order_item_repo, product_repo, user_repo,category_repo)
    return await order_service.create_order(order_create)

@order_router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order_update: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    order_item_repo = OrderItemRepository(db)
    order_item_service = OrderItemService(order_item_repo, product_repo, category_repo)
    order_service = OrderService(order_repo)
    return await order_service.update_order(order_id, order_update)

@order_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    order = await order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    success = await order_repo.delete(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}

@order_router.get("/", response_model=list[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    return await order_repo.get_all()