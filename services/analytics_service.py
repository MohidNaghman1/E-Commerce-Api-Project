from Repositories.analytics_repo import AnalyticsRepository

class AnalyticsService:
    def __init__(self, analytics_repo: AnalyticsRepository):
        self.analytics_repo = analytics_repo

    async def get_top_selling_products(self, limit: int = 10):
        rows = await self.analytics_repo.get_top_selling_products(limit)
        # Map tuples to response dicts
        return [
            {
                'product_id': row.product_id,
                'product_name': row.product_name,
                'total_sold': row.total_sold
            }
            for row in rows
        ]