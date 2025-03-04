from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional


T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[T]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self, *filters) -> List[T]:
        pass

    @abstractmethod
    def create(self, item_data: dict) -> Optional[T]:
        pass

    @abstractmethod
    def update(self, item_id: int, item_data: dict) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> Optional[T]:
        pass
