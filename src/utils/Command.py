from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass
