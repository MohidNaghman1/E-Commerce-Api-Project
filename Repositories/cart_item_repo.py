from .base_repo import BaseRepository
from models import CartItem
from sqlalchemy import select, delete



class CartItemRepository(BaseRepository):

    
    """
    Repository for CartItem model. Handles all database operations related to cart items.
    All methods are asynchronous and expect an async SQLAlchemy session.
    """

    def __init__(self, session):
        """
        Initialize repository with a database session.
        :param session: Async SQLAlchemy session
        """
        self.session = session

    async def add_to_cart(self, obj: CartItem) -> CartItem:
        """
        Add a new cart item to the database (no business logic, no commit).
        :param obj: CartItem instance
        :return: CartItem instance
        """
        self.session.add(obj)
        return obj
    async def get_by_user_and_product(self, user_id: int, product_id: int) -> CartItem | None:
        """
        Retrieve a cart item by user_id and product_id.
        :param user_id: User ID
        :param product_id: Product ID
        :return: CartItem instance or None if not found
        """
        result = await self.session.execute(
            select(CartItem).where(
                (CartItem.user_id == user_id) & (CartItem.product_id == product_id)
            )
        )
        return result.scalars().first()

    async def get_by_id(self, id: int) -> CartItem:
        """
        Retrieve a cart item by its ID.
        :param id: CartItem ID
        :return: CartItem instance or None if not found
        """
        result = await self.session.get(CartItem, id)
        return result
    async def get_cart_items_by_user_id(self, user_id: int) -> list[CartItem]:
        """
        Retrieve all cart items for a specific user.
        :param user_id: User ID
        :return: List of CartItem instances
        """
        result = await self.session.execute(select(CartItem).where(CartItem.user_id == user_id))
        return result.scalars().all()
    async def remove_from_cart(self, cart_item: CartItem) -> None:
        """
        Remove a cart item from the database.
        Commits the transaction after deletion.
        :param cart_item: CartItem instance to be removed
        """
        await self.session.delete(cart_item)


    async def update_cart_item(self, cart_item: CartItem) -> CartItem:
        """
        Update an existing cart item in the database.
        Commits and refreshes the object to get updated fields.
        :param cart_item: CartItem instance with updated data
        :return: Updated CartItem instance
        """
        self.session.add(cart_item)
        return cart_item
    
    async def clear_cart_by_user_id(self, user_id: int) -> None:
        """
        Remove all cart items for a specific user.
        Commits the transaction after deletion.
        :param user_id: User ID whose cart items are to be removed
        """
        await self.session.execute(
            delete(CartItem).where(CartItem.user_id == user_id)
        )