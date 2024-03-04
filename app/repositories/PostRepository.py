from abc import ABC, abstractmethod

from app.models.PostModel import Post


class PostRepository(ABC):
    @abstractmethod
    def new(self, new_row: Post) -> int:
        """
        Create a new post and returns the new id value.
        """
        pass

    @abstractmethod
    def get_by_id(self, id_val: int) -> Post:
        """
        Get a single post by ID value.
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Post]:
        """
        Get all posts.
        """
        pass
