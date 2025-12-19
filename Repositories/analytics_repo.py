from models import Product, OrderItem
from sqlalchemy import func, desc, select

class AnalyticsRepository:
    def __init__(self, session):
        self.session = session

    async def get_top_selling_products(self, limit: int = 10):
        stmt = (
            select(
                Product.id.label('product_id'),
                Product.name.label('product_name'),
                func.sum(OrderItem.quantity).label('total_sold')
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .group_by(Product.id, Product.name)
            .order_by(desc('total_sold'))
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        # Return list of tuples: (product_id, product_name, total_sold)
        return result.all()