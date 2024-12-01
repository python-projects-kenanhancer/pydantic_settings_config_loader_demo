import json
import logging
from typing import Any

from .config_loader import ConfigLoader
from .gcp_secret_loader import GcpSecretLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GcpSecretJsonLoader(GcpSecretLoader, ConfigLoader):

    # def __init__(self, secret_name: str, project_id: str):
    #     self.secret_name = secret_name
    #     self.project_id = project_id

    def load(self) -> dict[str, Any]:
        secret_payload = self.fetch_secret()
        if not secret_payload:
            raise ValueError("Failed to fetch secret payload.")
        try:
            return json.loads(secret_payload)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON secret: {e}")
            raise ValueError(f"Error parsing JSON secret: {e}")
