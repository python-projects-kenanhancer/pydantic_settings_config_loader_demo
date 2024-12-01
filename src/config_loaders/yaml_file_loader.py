from typing import Any

import yaml

from .config_loader import ConfigLoader


class YamlFileLoader(ConfigLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> dict[str, Any]:
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)
