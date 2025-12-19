from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import session as get_async_session
from Repositories.cart_item_repo import CartItemRepository
from Repositories.product_repo import ProductRepository
from Repositories.order_repo import OrderRepository
from Repositories.order_item_repo import OrderItemRepository
from services.cart_item_service import CartItemService
from services.checkout_service import CheckoutService
from schema.cart_item import CartItemCreate, CartItemUpdate, CartItemResponse

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_cart_item_service(session: AsyncSession = Depends(get_async_session)):
	return CartItemService(
		CartItemRepository(session),
		ProductRepository(session)
	)

def get_checkout_service(session: AsyncSession = Depends(get_async_session)):
	return CheckoutService(
		CartItemRepository(session),
		ProductRepository(session),
		OrderRepository(session),
		OrderItemRepository(session),
		session
	)

@router.post("/add", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
	cart_item: CartItemCreate,
	service: CartItemService = Depends(get_cart_item_service)
):
	return await service.add_to_cart(cart_item)

@router.patch("/update/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
	cart_item_id: int,
	cart_item_update: CartItemUpdate,
	service: CartItemService = Depends(get_cart_item_service)
):
	return await service.update_cart_item(cart_item_id, cart_item_update)

@router.delete("/remove/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
	cart_item_id: int,
	service: CartItemService = Depends(get_cart_item_service)
):
	await service.remove_from_cart(cart_item_id)

@router.get("/item/{cart_item_id}", response_model=CartItemResponse)
async def get_cart_item_by_id(
	cart_item_id: int,
	service: CartItemService = Depends(get_cart_item_service)
):
	return await service.get_cart_item_by_id(cart_item_id)

# Checkout endpoint
@router.post("/checkout/{user_id}", response_model=int)
async def checkout(
	user_id: int,
	service: CheckoutService = Depends(get_checkout_service)
):
	return await service.checkout(user_id)
