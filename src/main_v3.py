import logging
from logging import Logger

from config_loaders.decorators import (
    inject_settings_from_env_file,
    inject_settings_from_gcp_secret_env,
    inject_settings_from_gcp_secret_json,
    inject_settings_from_gcp_secret_yaml,
    inject_settings_from_gcp_storage_env,
    inject_settings_from_gcp_storage_json,
    inject_settings_from_gcp_storage_yaml,
    inject_settings_from_json_file,
    inject_settings_from_yaml_file,
)
from schemas import Settings


def configure_logging():
    """
    Configures logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,  # Set the default logging level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
        # handlers=[
        #     logging.StreamHandler(),  # Logs will be output to the console
        #     logging.FileHandler("cleanup.log"),  # Logs will also be written to cleanup.log
        # ],
    )


@inject_settings_from_env_file(file_path=".env")
def test_settings_from_env_file(logger: Logger, settings: Settings):
    logger.info(f"Settings from env file: {settings}")


@inject_settings_from_json_file(file_path="config.json")
def test_settings_from_json_file(logger: Logger, settings: Settings):
    logger.info(f"Settings from json file: {settings}")


@inject_settings_from_yaml_file(file_path="config.yaml")
def test_settings_from_yaml_file(logger: Logger, settings: Settings):
    logger.info(f"Settings from yaml file: {settings}")


@inject_settings_from_gcp_secret_env(secret_name="app-config-env", project_id="nexum-dev-364711")
def test_settings_from_gcp_secret_env(logger: Logger, settings: Settings):
    logger.info(f"Settings from gcp secret env file: {settings}")


@inject_settings_from_gcp_secret_json(secret_name="app-config-json", project_id="nexum-dev-364711")
def test_settings_from_gcp_secret_json(logger: Logger, settings: Settings):
    logger.info(f"Settings from gcp secret json file: {settings}")


@inject_settings_from_gcp_secret_yaml(secret_name="app-config-yaml", project_id="nexum-dev-364711")
def test_settings_from_gcp_secret_yaml(logger: Logger, settings: Settings):
    logger.info(f"Settings from gcp secret yaml file: {settings}")


@inject_settings_from_gcp_storage_env(bucket_name="app-config-boilerplate", blob_name=".env", project_id="nexum-dev-364711")
def test_settings_from_gcp_storage_env(logger: Logger, settings: Settings):
    logger.info(f"Settings from gcp storage env file: {settings}")


@inject_settings_from_gcp_storage_json(
    bucket_name="app-config-boilerplate", blob_name="config.json", project_id="nexum-dev-364711"
)
def test_settings_from_gcp_storage_json(logger: Logger, settings: Settings):
    logger.info(f"Settings from gcp storage json file: {settings}")


@inject_settings_from_gcp_storage_yaml(
    bucket_name="app-config-boilerplate", blob_name="config.yaml", project_id="nexum-dev-364711"
)
def test_settings_from_gcp_storage_yaml(logger: Logger, settings: Settings):
    logger.info(f"Settings from gcp storage yaml file: {settings}")


def main():
    configure_logging()

    logger = logging.getLogger(__name__)

    test_settings_from_env_file(logger)

    test_settings_from_json_file(logger)

    test_settings_from_yaml_file(logger)

    test_settings_from_gcp_secret_env(logger)

    test_settings_from_gcp_secret_json(logger)

    test_settings_from_gcp_secret_yaml(logger)

    test_settings_from_gcp_storage_env(logger)

    test_settings_from_gcp_storage_json(logger)

    test_settings_from_gcp_storage_yaml(logger)


if __name__ == "__main__":
    main()
