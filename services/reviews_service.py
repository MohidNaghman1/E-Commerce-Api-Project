from schema.reviews import ReviewCreate, ReviewUpdate
from models import Review, User, Product
from Repositories.reviews_repo import ReviewRepository
from Repositories.user_repo import UserRepository
from Repositories.product_repo import ProductRepository
from fastapi import HTTPException


class ReviewService:
    """
    Service layer for Review operations. Handles business logic and interacts with the ReviewRepository.
    All methods are asynchronous and expect an async SQLAlchemy session.
    """

    def __init__(self, session):
        """
        Initialize service with a database session.
        :param session: Async SQLAlchemy session
        """
        self.repo = ReviewRepository(session)
        self.user_repo = UserRepository(session)
        self.product_repo = ProductRepository(session)

    async def create_review(self, review_data: ReviewCreate) -> Review:
        """
        Create a new review.
        :param review_data: ReviewCreate schema instance
        :return: Created Review instance
        """
        # check if user exists and product exists
        user = await self.user_repo.get_by_id(review_data.user_id)
        product = await self.product_repo.get_by_id(review_data.product_id)
        if not user or not product:
            raise HTTPException(status_code=404, detail="User or Product not found")
           
            
        review_data = review_data.model_dump()
        new_review = Review(**review_data)
        try:
            return await self.repo.create(new_review)
        except Exception as e:
            # Log error or raise custom exception
            raise HTTPException(status_code=400, detail=f"Failed to create review: {str(e)}")
    
        


    async def get_review_by_id(self, review_id: int) -> Review:
        """
        Get a review by its ID.
        :param review_id: Review ID
        :return: Review instance
        """
        return await self.repo.get_by_id(review_id)

    async def get_all_reviews(self) -> list[Review]:
        """
        Get all reviews.
        :return: List of Review instances
        """
        return await self.repo.get_all()

    async def get_reviews_by_product_id(self, product_id: int) -> list[Review]:
        """
        Get all reviews for a specific product.
        :param product_id: Product ID
        :return: List of Review instances
        """
        return await self.repo.get_by_product_id(product_id)

    async def get_reviews_by_user_id(self, user_id: int) -> list[Review]:
        """
        Get all reviews made by a specific user.
        :param user_id: User ID
        :return: List of Review instances
        """
        return await self.repo.get_by_user_id(user_id)
    
    async def update_review(self, review_id: int, update_data: ReviewUpdate) -> Review:
        """
        Update an existing review.
        :param review_id: Review ID
        :param update_data: ReviewUpdate schema instance
        :return: Updated Review instance
        """
        review = await self.repo.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        # Optionally: check permissions here
        return await self.repo.update(review_id, update_data.model_dump(exclude_unset=True))
    
    async def delete_review(self, review_id: int) -> bool:
        """
        Delete a review by its ID.
        :param review_id: Review ID
        :return: True if deleted, False if not found
        """
        review = await self.repo.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return await self.repo.delete(review_id)