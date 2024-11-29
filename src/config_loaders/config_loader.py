from abc import ABC, abstractmethod


class ConfigLoader(ABC):
    @abstractmethod
    def load(self) -> dict:
        """Load configuration data and return as a dictionary."""
        pass
