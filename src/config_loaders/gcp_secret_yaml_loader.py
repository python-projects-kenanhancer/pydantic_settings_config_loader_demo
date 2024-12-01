import logging
from typing import Any

import yaml

from .config_loader import ConfigLoader
from .gcp_secret_loader import GcpSecretLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GcpSecretYamlLoader(GcpSecretLoader, ConfigLoader):

    # def __init__(self, secret_name: str, project_id: str):
    #     self.secret_name = secret_name
    #     self.project_id = project_id

    def load(self) -> dict[str, Any]:
        secret_payload = self.fetch_secret()
        if not secret_payload:
            raise ValueError("Failed to fetch secret payload.")
        try:
            return yaml.safe_load(secret_payload)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML secret: {e}")
            raise ValueError(f"Error parsing YAML secret: {e}")
