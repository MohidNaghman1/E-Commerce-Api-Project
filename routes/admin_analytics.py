from fastapi  import APIRouter, Depends
from Repositories.analytics_repo import AnalyticsRepository
from services.analytics_service import AnalyticsService
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db

router = APIRouter(prefix="/admin/analytics", tags=["Admin Analytics"])

@router.get("/top-selling-products")
async def get_top_selling_products(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    analytics_repo = AnalyticsRepository(db)
    analytics_service = AnalyticsService(analytics_repo)
    return await analytics_service.get_top_selling_products(limit)