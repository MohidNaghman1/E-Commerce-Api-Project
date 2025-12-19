from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.product_category_association import category_product_association


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    order_items = relationship("OrderItem", back_populates="product")
    category = relationship("Category",secondary=category_product_association, back_populates="products")
    reviews = relationship("Review", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")

    @property
    def average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 2)