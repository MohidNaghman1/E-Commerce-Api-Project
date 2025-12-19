from fastapi import APIRouter, Depends, HTTPException
from services.product_service import ProductService
from dependencies import get_db
from schema import ProductCreate, ProductUpdate, ProductResponse
from schema.products import ProductFiltering
from Repositories import ProductRepository, CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession


product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.post("/", response_model=ProductResponse)
async def create_product(product_create: ProductCreate, db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    category_repository = CategoryRepository(db)
    product_service = ProductService(product_repository,category_repository)
    return await product_service.create_product(product_create)

@product_router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    category_repository = CategoryRepository(db)
    product_service = ProductService(product_repository, category_repository)
    return await product_service.update_product(product_id, product_update)

@product_router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    product = await product_repository.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.get("/", response_model=list[ProductResponse])
async def get_all_products(filter:ProductFiltering = Depends(),db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    category_repository = CategoryRepository(db)

    product_service = ProductService(product_repository, category_repository)
    return await product_service.fetch_filtered_products(filter)

@product_router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    success = await product_repository.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}


@product_router.get("/{product_id}/average-rating")
async def get_average_rating(product_id: int, db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    product = await product_repository.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, "average_rating": product.average_rating}