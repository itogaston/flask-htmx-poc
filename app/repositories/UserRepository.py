from abc import ABC, abstractmethod

from app.models.UserModel import User


class UserRepository(ABC):
    @abstractmethod
    def new(self, new_row: User) -> int:
        """
        Create a new record and returns the new id value.
        """
        pass

    @abstractmethod
    def get_by_id(self, id_val: int) -> User:
        """
        Get a single record by ID value.
        """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User:
        """
        Get a single record by username value.
        """
        pass
