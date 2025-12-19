from fastapi import APIRouter, Depends, HTTPException
from services.orderitem_service import OrderItemService
from Repositories import OrderItemRepository, ProductRepository,CategoryRepository, OrderRepository
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schema import OrderItemCreate, OrderItemResponse, OrderItemUpdate



order_item_router = APIRouter(prefix="/order-items", tags=["order-items"])


@order_item_router.post("/", response_model=OrderItemResponse)
async def create_order_item(
    order_item_create: OrderItemCreate,
    db: AsyncSession = Depends(get_db),
):
    order_item_repo = OrderItemRepository(db)
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    order_repo = OrderRepository(db)
    order_item_service = OrderItemService(order_item_repo, product_repo, category_repo, order_repo)
    return await order_item_service.create_order_item(order_item_create)


@order_item_router.put("/{order_item_id}", response_model=OrderItemResponse)
async def update_order_item(
    order_item_id: int,
    order_item_update: OrderItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    order_item_repo = OrderItemRepository(db)
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    order_repo = OrderRepository(db)
    order_item_service = OrderItemService(order_item_repo, product_repo, category_repo, order_repo) 
    return await order_item_service.update_order_item(order_item_id, order_item_update)

@order_item_router.get("/{order_item_id}", response_model=OrderItemResponse)
async def get_order_item(
    order_item_id: int,
    db: AsyncSession = Depends(get_db),
):
    order_item_repo = OrderItemRepository(db)
    order_item = await order_item_repo.get_by_id(order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item

@order_item_router.get("/", response_model=list[OrderItemResponse])
async def get_all_order_items(db: AsyncSession = Depends(get_db)):
    order_item_repo = OrderItemRepository(db)
    return await order_item_repo.get_all()

@order_item_router.delete("/{order_item_id}")
async def delete_order_item(
    order_item_id: int,
    db: AsyncSession = Depends(get_db),
):
    order_item_repo = OrderItemRepository(db)
    success = await order_item_repo.delete(order_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"detail": "Order item deleted successfully"}