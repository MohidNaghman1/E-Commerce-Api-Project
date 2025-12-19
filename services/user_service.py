
from Repositories import UserRepository
from models import User
from schema import UserCreate, UserUpdate
from fastapi import HTTPException
from hashlib import sha256

class UserService:
    """
    Service layer for user-related business logic.
    Handles user creation and updates with validation and password security.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user after validating uniqueness of email and username.
        Password is hashed before storing for security.
        """
        # Check for existing user by email
        existing_user_by_email = await self.repository.get_by_email(user_create.email)
        if existing_user_by_email:
            # Optionally raise custom error
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Check for existing user by username
        if user_create.name:
            existing_user_by_username = await self.repository.get_by_username(user_create.name)
            if existing_user_by_username:
                raise HTTPException(status_code=400, detail="User with this username already exists")
            
        # Hash the password before storing
        if hasattr(user_create, "password") and user_create.password:
            hashed_password = sha256(user_create.password.encode()).hexdigest()
            user_create.hashed_password = hashed_password
            # Optionally remove plain password attribute if present
            if hasattr(user_create, "password"):
                delattr(user_create, "password")

        user_data = user_create.model_dump()
        user = User(**user_data)
        return await self.repository.create(user)

    async def user_update(self, user_id: int, user_update: UserUpdate) -> User:
        """
        Update an existing user's fields. Hashes password if updated.
        """
        existing_user = await self.repository.get_by_id(user_id)
        if not existing_user:
            raise ValueError("User not found")
        update_data = user_update.model_dump(exclude_unset=True)
        # Hash password if being updated
        if "password" in update_data:
            hashed_password = sha256(update_data["password"].encode()).hexdigest()
            update_data["hashed_password"] = hashed_password
            del update_data["password"]
        return await self.repository.update(user_id, update_data)