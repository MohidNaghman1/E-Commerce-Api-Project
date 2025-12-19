from models import OrderItem
from Repositories import OrderItemRepository, ProductRepository,CategoryRepository
from schema.order_item import OrderItemCreate
from services.product_service import ProductService
from schema.order_item import OrderItemUpdate
from fastapi import HTTPException



class OrderItemService:
    """
    Service layer for order item-related business logic.
    Handles creation and updates of order items, including stock management.
    """

    def __init__(self, order_item_repository: OrderItemRepository, product_repo: ProductRepository, category_repo: CategoryRepository, order_repo=None):
        self.order_item_repository = order_item_repository
        self.product_service = ProductService(product_repo, category_repo)
        self.order_repo = order_repo
        if order_repo:
            from services.order_service import OrderService
            self.order_service = OrderService(order_repo, order_item_repository, product_repo, None, category_repo)
        else:
            self.order_service = None
    async def create_order_item(self, order_item_create: OrderItemCreate) -> OrderItem:
        """
        Create a new order item after validating product existence and stock.
        Reduces product stock accordingly.
        WARNING: No transaction/rollback if order item creation fails after stock reduction.
        """
        # Validate product existence
        product = await self.product_service.product_repository.get_by_id(order_item_create.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check stock availability
        if product.stock < order_item_create.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock for the product")

        # Reduce stock
        await self.product_service.manage_stock(product.id, -order_item_create.quantity)

        # Create OrderItem
        order_item = OrderItem(
            order_id=order_item_create.order_id,
            product_id=order_item_create.product_id,
            quantity=order_item_create.quantity,
            price=product.price,  # fetch price from product
        )
        created_item = await self.order_item_repository.create(order_item)
        if self.order_service and order_item_create.order_id:
            await self.order_service.recalculate_total(order_item_create.order_id)
        return created_item
    async def update_order_item(self, item_id: int, item_update: OrderItemUpdate) -> OrderItem:
        """
        Update an order item's fields. Adjusts stock if quantity changes.
        WARNING: No transaction/rollback if stock update or item update fails.
        """
        order_item = await self.order_item_repository.get_by_id(item_id)
        if not order_item:
            raise HTTPException(status_code=404, detail="Order item not found")
        update_data = item_update.model_dump(exclude_unset=True)

        # If quantity changes, adjust stock
        if "quantity" in update_data:
            quantity_diff = update_data["quantity"] - order_item.quantity
            await self.product_service.manage_stock(order_item.product_id, -quantity_diff)

    
        updated_item = await self.order_item_repository.update(item_id, update_data)
        if self.order_service and order_item.order_id:
            await self.order_service.recalculate_total(order_item.order_id)
        return updated_item