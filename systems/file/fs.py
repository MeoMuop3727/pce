from abc import ABC, abstractmethod
from typing import Any

class FileSystem(ABC):

    @abstractmethod
    def exists(self, path: str) -> bool: ...

    @abstractmethod
    def read(self, path: str) -> Any: ...

    @abstractmethod
    def write(self, path: str, data: Any) -> None: ...

    @abstractmethod
    def update(self, path: str, data: Any) -> None: ...

    @abstractmethod
    def delete(self, path: str) -> None: ...

    @abstractmethod
    def create(self, path: str, data: Any) -> None: ...

