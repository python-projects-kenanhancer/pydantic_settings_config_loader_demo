import logging

from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import SecretManagerServiceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GcpSecretLoader:
    """
    Base class for fetching secrets from Google Cloud Secret Manager.
    Returns the secret as a raw string.
    """

    def __init__(self, secret_name: str, project_id: str):
        self.secret_name = secret_name
        self.project_id = project_id

    def fetch_secret(self) -> str | None:
        """
        Fetches the raw secret data from Google Cloud Secret Manager.
        """
        try:
            client = SecretManagerServiceClient()
            # secret_path = f"projects/{self.project_id}/secrets/{self.secret_name}/versions/latest"
            secret_path = client.secret_version_path(self.project_id, self.secret_name, "latest")
            response = client.access_secret_version(name=secret_path)  # type: ignore
            logger.info(f"Successfully fetched secret: {self.secret_name}")
            return response.payload.data.decode("UTF-8")
        except DefaultCredentialsError as e:
            logger.error(f"Error loading credentials: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred while fetching secret: {self.secret_name}")
            return None
