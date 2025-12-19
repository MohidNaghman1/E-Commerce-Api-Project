from fastapi import APIRouter, Depends, HTTPException
from services.user_service import UserService
from Repositories import UserRepository
from dependencies import get_db
from schema import UserCreate, UserUpdate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=UserResponse)
async def create_user(user_create: UserCreate, db: AsyncSession  = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    print("USER SESSION:", id(db))
    return await user_service.create_user(user_create)

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    return await user_service.user_update(user_id, user_update)

@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    return await user_repo.get_all()

@user_router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    success = await user_repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}