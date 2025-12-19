from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    product_id: int
    user_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    product_id: int
    user_id: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)