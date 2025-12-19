from .base_repo import BaseRepository
from sqlalchemy.future import select
from models import User



class UserRepository(BaseRepository):
    """
    Repository for User model. Handles all database operations for users.
    """

    def __init__(self, session):
        self.session = session

    async def create(self, obj: User) -> User:
        """
        Add a new user to the database and return the created user.
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id: int) -> User:
        """
        Retrieve a user by their ID. Returns None if not found.
        """
        result = await self.session.get(User, id)
        return result

    async def get_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email. Returns None if not found.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_all(self) -> list[User]:
        """
        Retrieve all users from the database.
        """
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def update(self, id: int, update_data: dict) -> User:
        """
        Update an existing user with the provided fields. Returns updated user or None.
        """
        existing_user = await self.get_by_id(id)
        if not existing_user:
            return None
        for key, value in update_data.items():
            setattr(existing_user, key, value)
        self.session.add(existing_user)
        await self.session.commit()
        await self.session.refresh(existing_user)
        return existing_user

    async def delete(self, id: int) -> bool:
        """
        Delete a user by ID. Returns True if deleted, False if not found.
        """
        existing_user = await self.get_by_id(id)
        if not existing_user:
            return False
        await self.session.delete(existing_user)
        await self.session.commit()
        return True

    async def get_by_username(self, username: str) -> User:
        """
        Retrieve a user by their username. Returns None if not found.
        """
        result = await self.session.execute(
            select(User).where(User.name == username)
        )
        return result.scalars().first()

