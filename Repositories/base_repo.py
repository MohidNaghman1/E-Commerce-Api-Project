from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar('T')
ID = TypeVar('ID')

class BaseRepository(ABC, Generic[T, ID]):
    """
    Abstract base class for repositories. Defines the CRUD interface for all repositories.
    """

    @abstractmethod
    async def create(self, obj: T) -> T:
        """
        Create a new object in the database.
        :param obj: The object to create
        :return: The created object
        """
        pass

    @abstractmethod
    async def get_by_id(self, id: ID) -> Optional[T]:
        """
        Retrieve an object by its ID.
        :param id: The ID of the object
        :return: The object if found, else None
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        """
        Retrieve all objects from the database.
        :return: List of all objects
        """
        pass

    @abstractmethod
    async def update(self, id: ID, obj: T) -> Optional[T]:
        """
        Update an existing object by its ID.
        :param id: The ID of the object
        :param obj: The object with updated data
        :return: The updated object if found, else None
        """
        pass

    @abstractmethod
    async def delete(self, id: ID) -> bool:
        """
        Delete an object by its ID.
        :param id: The ID of the object
        :return: True if deleted, False otherwise
        """
        pass