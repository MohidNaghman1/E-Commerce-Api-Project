from schema import ProductCreate, ProductUpdate
from schema.products import ProductFiltering
from models import Product
from Repositories import ProductRepository,CategoryRepository
from fastapi import HTTPException


class ProductService:
    """
    Service layer for product-related business logic.
    Handles product creation, updates, and stock management with validation.
    """

    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def create_product(self, product_create: ProductCreate) -> Product:
        """
        Create a new product after validating uniqueness and category existence.
        """
        # Check for existing product by name
        existing_product = await self.product_repository.get_product_by_name(product_create.name)
        if existing_product:
            raise HTTPException(status_code=400, detail="Product with this name already exists")
        
        data = product_create.model_dump(exclude={"category_ids"})
        new_product = Product(**data)
        # Validate category existence
        if product_create.category_ids:
            for category_id in product_create.category_ids:
                category = await self.category_repository.get_by_id(category_id)
                if not category:
                    raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")
                
                categories = await self.category_repository.get_by_ids(product_create.category_ids)
                new_product.categories = categories
                
       
        return await self.product_repository.create(new_product)

    async def update_product(self, id: int, product_update: ProductUpdate) -> Product:
        """
        Update an existing product's fields. Validates category if changed.
        """
        existing_product = await self.product_repository.get_by_id(id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")

        update_data = product_update.model_dump(exclude_unset=True)

        # Validate new category if being updated
        if "category_id" in update_data:
            category = await self.category_repository.get_by_id(update_data["category_id"])
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")

        return await self.product_repository.update(id, update_data)


    async def fetch_filtered_products(self, filters: ProductFiltering) -> list[Product]:
        """
        Retrieve products based on filtering criteria.
        """
        return await self.product_repository.fetch_filtered(filters)
    

    

