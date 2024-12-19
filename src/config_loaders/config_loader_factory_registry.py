import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from .config_loader import ConfigLoader
from .config_loader_args import ConfigLoaderArgs

T = TypeVar("T", bound="ConfigLoaderArgs")


class ConfigLoaderFactoryRegistry:
    """
    A hybrid factory class for creating configuration loaders.
    """

    _default_instance: Optional["ConfigLoaderFactoryRegistry"] = None

    def __init__(self):
        """
        Initialize a ConfigLoaderFactory with an empty registry.
        """
        self._loader_registry: Dict[Type[Any], Callable[[Any], ConfigLoader]] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("ConfigLoaderFactory initialized with an empty registry.")

    @classmethod
    def default(cls) -> "ConfigLoaderFactoryRegistry":
        """
        Retrieve the default factory instance, creating it if necessary.
        """
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance

    def register(self, args_type: Type[T], constructor: Callable[[T], ConfigLoader]) -> None:
        """
        Register a loader constructor for a specific argument type.

        :param args_type: The type of arguments for the loader.
        :param constructor: A callable that accepts `args` and returns a ConfigLoader instance.
        """
        if args_type in self._loader_registry:
            self.logger.warning(f"Overwriting existing loader registration for: {args_type}")
        self._loader_registry[args_type] = constructor
        self.logger.info(f"Registered loader for args type: {args_type}")

    def get_loader(self, args: ConfigLoaderArgs) -> ConfigLoader:
        """
        Create a loader based on the provided arguments.

        :param args: Arguments specifying the loader type and details.
        :return: An instance of the appropriate loader.
        :raises ValueError: If no loader is registered for the argument type.
        """
        args_type = type(args)  # Dynamically determine the type of `args`
        constructor = self._loader_registry.get(args_type)

        if not constructor:
            self.logger.error(f"No loader registered for argument type: {args_type}")
            raise ValueError(f"Unsupported loader arguments: {args_type}")

        try:
            loader = constructor(args)  # Pass `args` to the constructor
            self.logger.info(f"Created loader: {loader.__class__.__name__} for args: {args}")
            return loader
        except Exception:
            self.logger.exception(f"Failed to create loader for args: {args}")
            raise
