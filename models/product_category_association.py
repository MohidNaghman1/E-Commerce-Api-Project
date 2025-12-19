from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base



# Association table for many-to-many relationship between Category and Product
category_product_association = Table(
    "category_product",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True)
)