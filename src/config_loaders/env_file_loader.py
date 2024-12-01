import json
import os
from typing import Any

from dotenv import dotenv_values

from .config_loader import ConfigLoader


class EnvFileLoader(ConfigLoader):
    """
    Loads configuration from an environment file, supports nested keys
    and JSON parsing for string values.
    """

    def __init__(self, file_path: str):
        """
        Initialize the EnvFileLoader with the file path.
        :param file_path: Path to the .env file to be loaded.
        """
        self.file_path = file_path

    def _parse_json_fields(self, nested_env: dict[str, str | dict[str, Any]]) -> None:
        """
        Recursively parse JSON strings in a nested dictionary.
        :param nested_env: Nested dictionary to process.
        """
        for key, value in nested_env.items():
            if isinstance(value, dict):
                # Recursively handle nested dictionaries
                self._parse_json_fields(value)
            else:
                try:
                    # Attempt to parse JSON strings
                    nested_env[key] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    # Skip non-JSON strings
                    pass

    def _nest_dict(self, flat_dict: dict[str, str | Any]) -> dict[str, Any]:
        """
        Transform a flat dictionary with double underscores into nested dictionaries.
        :param flat_dict: Flat dictionary to transform.
        :return: Nested dictionary.
        """
        nested: dict[str, Any] = {}  # Explicitly type the nested dictionary

        for key, value in flat_dict.items():
            keys = key.lower().split("__")  # Use double underscores to create nested keys
            current_level = nested

            for part in keys[:-1]:
                if part not in current_level or not isinstance(current_level[part], dict):
                    current_level[part] = {}  # Ensure the current level is a dictionary
                current_level = current_level[part]  # Move to the next level

            current_level[keys[-1]] = value  # Assign the value to the final key

        return nested

    def load(self) -> dict[str, Any]:
        """
        Load and process the .env file, returning the parsed nested configuration.
        :return: Nested dictionary of configuration.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Configuration file not found at path: {self.file_path}")

        # Load raw .env values
        raw_env = dotenv_values(self.file_path)

        # Transform into a nested dictionary
        nested_env = self._nest_dict(raw_env)

        # Parse JSON fields in the nested dictionary
        self._parse_json_fields(nested_env)

        return nested_env
