from models import OrderItem,Order
from Repositories import OrderItemRepository,ProductRepository,OrderRepository,UserRepository,CategoryRepository
from schema import OrderCreate, OrderUpdate
from fastapi import HTTPException
from services.orderitem_service import OrderItemService
from schema.order_item import OrderItemCreate
from services.inventory_serivce import InventoryService
import asyncio
from schema.orders import OrderStatus


class OrderService:
    """
    Service layer for handling order-related business logic.
    Handles order creation, validation, and updates with transaction safety.
    """

    def __init__(self, order_repo: OrderRepository, order_item_repo: OrderItemRepository, product_repo: ProductRepository, user_repo: UserRepository,category_repo=CategoryRepository):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.product_repo = product_repo
        self.user_repo = user_repo
        self.category_repo = category_repo
        self.order_item_service = OrderItemService(order_item_repo, product_repo, category_repo)
        self.inventory_service = InventoryService(product_repo)

    async def _calculate_total(self, order_id: int) -> int:
        items = await self.order_item_repo.get_by_order_id(order_id)
        return sum(item.quantity * item.price for item in items)

 
    async def recalculate_total(self, order_id: int):
        total = await self._calculate_total(order_id)
        await self.order_repo.update(order_id, {"total": total})


    async def create_order(self, order_create: OrderCreate) -> Order:
        """
        Create order and order items atomically with transaction safety.
        Validates all products and quantities, reduces stock, creates order and items.
        Rolls back if anything fails.
        After order creation, triggers low_stock_alerts as a background task (non-blocking).
        """
        # 1. Validate user
        user = await self.user_repo.get_by_id(order_create.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 2. Validate all products and quantities first (no stock is reduced yet)
        products = await self.inventory_service.validate_products_and_quantities(order_create.items)

        session = self.order_repo.session
        async with session.begin():
            # 3. Reduce stock for all products (now that all are validated)
            await self.inventory_service.reduce_stock(order_create.items, session, products=products)

            # 4. Create empty order
            order = Order(
                user_id=order_create.user_id,
                status=order_create.status,
                total=0
            )
            session.add(order)
            await session.flush()  # get order.id

            # 5. Create order items & calculate total
            total = 0
            for item in order_create.items:
                product = products[item.product_id]
                item_total = product.price * item.quantity
                total += item_total
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price
                )
                session.add(order_item)

            # 6. Update order total
            order.total = total
            session.add(order)
            await session.flush()

        # 7. Trigger low_stock_alerts as a background task (non-blocking)
        asyncio.create_task(self.inventory_service.low_stock_alerts())

        # 8. Reload order with items (outside transaction)
        return await self.order_repo.get_by_id(order.id)


    async def update_order(self, order_id: int, order_update: OrderUpdate) -> Order:
        """
        Update an existing order's fields, with status transition validation.
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        update_data = order_update.model_dump(exclude_unset=True)

        # Validate status transition if status is being updated
        if "status" in update_data:
        
            current_status = order.status
            new_status = update_data["status"]
            allowed_transitions = {
                OrderStatus.pending: [OrderStatus.paid],
                OrderStatus.paid: [OrderStatus.shipped],
                OrderStatus.shipped: [OrderStatus.delivered],
                OrderStatus.delivered: [],
            }
            if new_status == current_status:
                pass  # No change
            elif new_status not in allowed_transitions.get(current_status, []):
                raise HTTPException(status_code=400, detail=f"Invalid status transition: {current_status} → {new_status}")

        return await self.order_repo.update(order_id, update_data)