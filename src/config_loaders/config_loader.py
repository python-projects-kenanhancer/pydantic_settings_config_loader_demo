from abc import ABC, abstractmethod
from typing import Any


class ConfigLoader(ABC):
    @abstractmethod
    def load(self) -> dict[str, Any]:
        """Load configuration data and return as a dictionary."""
        pass
