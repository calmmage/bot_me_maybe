from abc import abstractmethod, ABC
from typing import Any, Dict, List


class DatabaseInterface(ABC):
    @abstractmethod
    def put(self, table: str, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get(self, table: str, key: str) -> Any:
        pass

    @abstractmethod
    def edit(self, table: str, key: str, new_value: Any) -> None:
        pass

    @abstractmethod
    def delete(self, table: str, key: str) -> None:
        pass

    @abstractmethod
    def bulk_put(self, table: str, items: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def bulk_get(self, table: str, keys: List[str]) -> Dict[str, Any]:
        pass