from abc import ABC, abstractmethod
from typing import Any

class Serializer(ABC):

    @abstractmethod
    def encode(self, data: Any) -> bytes: ...

    @abstractmethod
    def decode(self, data: bytes) -> Any: ...

