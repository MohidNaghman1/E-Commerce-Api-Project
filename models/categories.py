from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.product_category_association import category_product_association




class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    products = relationship(
        "Product",
        secondary=category_product_association,
        back_populates="category")