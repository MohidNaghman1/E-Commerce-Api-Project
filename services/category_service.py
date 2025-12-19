from models import Category
from Repositories import CategoryRepository
from schema import CategoryCreate, CategoryUpdate
from fastapi import HTTPException


class CategoryService:
    """
    Service layer for category-related business logic.
    Handles category creation and updates with validation.
    """

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, category_create: CategoryCreate) -> Category:
        """
        Create a new category after validating uniqueness by name.
        """
        # Check for existing category by name
        existing_category = await self.repo.get_by_name(category_create.name)
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        
        new_category = Category(**category_create.model_dump())
        return await self.repo.create(new_category)

    async def update_category(self, category_id: int, category_update: CategoryUpdate) -> Category:
        """
        Update an existing category's fields. Only updates provided fields.
        """
        existing_category = await self.repo.get_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data = category_update.model_dump(exclude_unset=True)
        return await self.repo.update(category_id, update_data)
