from fastapi import HTTPException


from services.inventory_serivce import InventoryService

class CheckoutService:
    def __init__(self, cart_item_repo, product_repo, order_repo, order_item_repo, session):
        self.cart_item_repo = cart_item_repo
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.session = session
        self.inventory_service = InventoryService(product_repo)

    async def checkout(self, user_id: int) -> int:
        """
        Atomically checkout all cart items for a user:
        - Validate stock for all items
        - Fail if any item is insufficient
        - Reduce stock
        - Create order and order_items
        - Clear cart
        - Commit ONCE
        Returns: order_id
        """
        # 1. Read all cart items
        cart_items = await self.cart_item_repo.get_cart_items_by_user_id(user_id)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # 2. Validate stock for all items using InventoryService
        products = await self.inventory_service.validate_products_and_quantities(cart_items)

        # 3. Calculate total
        total = sum(products[item.product_id].price * item.quantity for item in cart_items)

        # 4. Begin transaction
        async with self.session.begin():
            # 5. Reduce stock for all products using InventoryService
            await self.inventory_service.reduce_stock(cart_items, self.session, products=products)

            # 6. Create order
            from models import Order, OrderItem
            order = Order(user_id=user_id, total=total, status="pending")
            self.session.add(order)
            await self.session.flush()  # get order.id

            # 7. Create order_items
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity
                )
                self.session.add(order_item)

            # 8. Clear cart
            await self.cart_item_repo.clear_cart_by_user_id(user_id)

        return order.id
