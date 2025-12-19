from models import CartItem, Product
from fastapi import HTTPException, status
from sqlalchemy import select
from Repositories.cart_item_repo import CartItemRepository
from Repositories.product_repo import ProductRepository
from schema.cart_item import CartItemCreate, CartItemUpdate, CartItemResponse

class CartItemService:
    def __init__(self, cart_item_repo: CartItemRepository, product_repo: ProductRepository):
        self.cart_item_repo = cart_item_repo
        self.product_repo = product_repo

    async def add_to_cart(self, cart_item_create: CartItemCreate) -> CartItemResponse:
        product = await self.product_repo.get_by_id(cart_item_create.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Check if the product is already in the user's cart (no stock check)
        existing_item = await self.cart_item_repo.get_by_user_and_product(
            cart_item_create.user_id, cart_item_create.product_id
        )
        if existing_item:
            existing_item.quantity += cart_item_create.quantity
            self.cart_item_repo.session.add(existing_item)
            await self.cart_item_repo.session.commit()
            await self.cart_item_repo.session.refresh(existing_item)
            return CartItemResponse.model_validate(existing_item)
        else:
            cart_item = CartItem(**cart_item_create.model_dump())
            await self.cart_item_repo.add_to_cart(cart_item)
            await self.cart_item_repo.session.commit()
            await self.cart_item_repo.session.refresh(cart_item)
            return CartItemResponse.model_validate(cart_item)
    
    async def remove_from_cart(self, cart_item_id: int) -> None:
        cart_item = await self.cart_item_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        
        await self.cart_item_repo.remove_from_cart(cart_item)

    async def update_cart_item(self, cart_item_id: int, cart_item_update: CartItemUpdate) -> CartItemResponse:
        cart_item = await self.cart_item_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        if cart_item_update.quantity is not None:
            cart_item.quantity = cart_item_update.quantity
        updated_cart_item = await self.cart_item_repo.update_cart_item(cart_item)
        await self.cart_item_repo.session.commit()
        await self.cart_item_repo.session.refresh(updated_cart_item)
        return CartItemResponse.model_validate(updated_cart_item)
    
    async def get_cart_item_by_id(self, cart_item_id: int) -> CartItemResponse:
        cart_item = await self.cart_item_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        
        return CartItemResponse.model_validate(cart_item)