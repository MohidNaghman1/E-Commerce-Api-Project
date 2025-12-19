from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    hashed_password: str
    role: Optional[str] = "customer"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)