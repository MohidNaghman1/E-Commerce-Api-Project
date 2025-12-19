from fastapi import APIRouter, Depends, HTTPException
from services.reviews_service import ReviewService
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schema import ReviewCreate, ReviewUpdate, ReviewResponse

review_router = APIRouter(prefix="/reviews", tags=["reviews"])

@review_router.post("/", response_model=ReviewResponse)
async def create_review(review_create: ReviewCreate, db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    return await review_service.create_review(review_create)

@review_router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@review_router.get("/", response_model=list[ReviewResponse])
async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    return await review_service.get_all_reviews()

@review_router.get("/product/{product_id}", response_model=list[ReviewResponse])
async def get_reviews_by_product(product_id: int, db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    return await review_service.get_reviews_by_product_id(product_id)

@review_router.get("/user/{user_id}", response_model=list[ReviewResponse])
async def get_reviews_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    return await review_service.get_reviews_by_user_id(user_id)

@review_router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(review_id: int, review_update: ReviewUpdate, db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    return await review_service.update_review(review_id, review_update)

@review_router.delete("/{review_id}")
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review_service = ReviewService(db)
    await review_service.delete_review(review_id)
    return {"detail": "Review deleted successfully"}