import json

from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import SecretManagerServiceClient

from .config_loader import ConfigLoader


class GcpSecretLoader(ConfigLoader):
    def __init__(self, secret_name: str, project_id: str):
        self.secret_name = secret_name
        self.project_id = project_id

    def load(self) -> dict:
        try:
            client = SecretManagerServiceClient()
            secret_path = f"projects/{self.project_id}/secrets/{self.secret_name}/versions/latest"
            response = client.access_secret_version(name=secret_path)
            secret_payload = response.payload.data.decode("UTF-8")
            return json.loads(secret_payload)
        except DefaultCredentialsError as e:
            print(f"Error loading credentials: {e}")
            # Handle the error appropriately
            return {}
