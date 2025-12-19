from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total = Column(Integer, nullable=False)
    status = Column(String, default="pending", nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat(), nullable=False)


    
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")