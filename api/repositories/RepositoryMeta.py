from abc import abstractmethod
from typing import Generic, List, TypeVar

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")


#################################
# Abstract Class for Repository #
#################################
class RepositoryMeta(Generic[M, K]):

    # Create a new instance of the Model
    @abstractmethod
    def create(self, instance: M) -> M:
        pass

    # Fetch an existing instance of the Model by it's unique Id
    @abstractmethod
    def get(self, id: K) -> M:
        pass

    # Lists all existing instance of the Model
    @abstractmethod
    def list(self, limit: int, start: int) -> (int, List[M]):
        pass

    # Updates an existing instance of the Model
    @abstractmethod
    def update(self, id: K, instance: M) -> M:
        pass