from fastapi import APIRouter, Depends, HTTPException
from services.category_service import CategoryService
from Repositories import CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from schema import CategoryCreate, CategoryUpdate, CategoryResponse


category_router = APIRouter(prefix="/categories", tags=["categories"])

@category_router.post("/", response_model=CategoryResponse)
async def create_category(category_create: CategoryCreate, db: AsyncSession = Depends(get_db)):
    create_category = CategoryRepository(db)
    category_service = CategoryService(create_category)
    return await category_service.create_category(category_create)

@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category_update: CategoryUpdate, db: AsyncSession
= Depends(get_db)):
    create_category = CategoryRepository(db)
    category_service = CategoryService(create_category)
    return await category_service.update_category(category_id, category_update)

@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    create_category = CategoryRepository(db)
    category = await create_category.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@category_router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    create_category = CategoryRepository(db)
    return await create_category.get_all()

@category_router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    create_category = CategoryRepository(db)
    success = await create_category.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}

