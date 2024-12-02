from abc import ABC, abstractmethod
from typing import Any


class EnvProcessor(ABC):
    @abstractmethod
    def process(self, flat_dict: dict[str, str | Any]) -> dict[str, Any]:
        pass
