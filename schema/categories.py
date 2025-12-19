from pydantic import BaseModel,ConfigDict

class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str
    description: str

class CategoryResponse(CategoryBase):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
