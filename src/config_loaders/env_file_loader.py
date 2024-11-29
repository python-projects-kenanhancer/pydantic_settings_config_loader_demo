import json
import os
from collections import defaultdict

from dotenv import dotenv_values

from .config_loader import ConfigLoader


class EnvFileLoader(ConfigLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _parse_json_fields(self, nested_env):
        """Recursively parse JSON strings in a nested dictionary."""
        for key, value in nested_env.items():
            if isinstance(value, dict):
                # Recursively handle nested dictionaries
                self._parse_json_fields(value)
            elif isinstance(value, str):
                try:
                    # Attempt to parse JSON strings
                    nested_env[key] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    # Skip non-JSON strings
                    pass

    def _nest_dict(self, flat_dict):
        """Transform flat dictionary with double underscores into nested dictionaries."""
        nested = defaultdict(dict)
        for key, value in flat_dict.items():
            keys = key.lower().split("__")  # Use double underscores to create nested keys
            current_level = nested
            for part in keys[:-1]:
                current_level = current_level.setdefault(part, {})
            current_level[keys[-1]] = value
        return nested

    def load(self) -> dict:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Configuration file not found at path: {self.file_path}")
        raw_env = dotenv_values(self.file_path)
        nested_env = self._nest_dict(raw_env)
        self._parse_json_fields(nested_env)
        return nested_env
