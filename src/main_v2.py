import logging
from typing import TypedDict

from config_loaders import (
    ConfigLoaderFactoryRegistry,
    DefaultEnvConfigProcessor,
    EnvConfigLoader,
    JsonConfigLoader,
    YamlConfigLoader,
)
from config_loaders.config_loader_args import (
    ConfigLoaderArgs,
    EnvConfigLoaderArgs,
    GcpSecretEnvConfigLoaderArgs,
    GcpSecretJsonConfigLoaderArgs,
    GcpSecretYamlConfigLoaderArgs,
    GcpStorageEnvConfigLoaderArgs,
    GcpStorageJsonConfigLoaderArgs,
    GcpStorageYamlConfigLoaderArgs,
    JsonConfigLoaderArgs,
    YamlConfigLoaderArgs,
)
from config_loaders.config_providers import FileConfigProvider, GcpSecretConfigProvider, GcpStorageConfigProvider
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


def register_loaders(factory: ConfigLoaderFactoryRegistry) -> None:
    """
    Register all necessary loaders with the factory.
    """
    factory.register(
        GcpSecretEnvConfigLoaderArgs,
        lambda config_loader_args: EnvConfigLoader(
            config_provider=GcpSecretConfigProvider(
                secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
            ),
            env_processor=DefaultEnvConfigProcessor(),
        ),
    )

    factory.register(
        GcpSecretJsonConfigLoaderArgs,
        lambda config_loader_args: JsonConfigLoader(
            config_provider=GcpSecretConfigProvider(
                secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
            )
        ),
    )

    factory.register(
        GcpSecretYamlConfigLoaderArgs,
        lambda config_loader_args: YamlConfigLoader(
            config_provider=GcpSecretConfigProvider(
                secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
            )
        ),
    )

    factory.register(
        GcpStorageEnvConfigLoaderArgs,
        lambda config_loader_args: EnvConfigLoader(
            config_provider=GcpStorageConfigProvider(
                bucket_name=config_loader_args.bucket_name,
                blob_name=config_loader_args.blob_name,
                project_id=config_loader_args.project_id,
            ),
            env_processor=DefaultEnvConfigProcessor(),
        ),
    )

    factory.register(
        GcpStorageJsonConfigLoaderArgs,
        lambda config_loader_args: JsonConfigLoader(
            config_provider=GcpStorageConfigProvider(
                bucket_name=config_loader_args.bucket_name,
                blob_name=config_loader_args.blob_name,
                project_id=config_loader_args.project_id,
            )
        ),
    )

    factory.register(
        GcpStorageYamlConfigLoaderArgs,
        lambda config_loader_args: YamlConfigLoader(
            config_provider=GcpStorageConfigProvider(
                bucket_name=config_loader_args.bucket_name,
                blob_name=config_loader_args.blob_name,
                project_id=config_loader_args.project_id,
            )
        ),
    )

    factory.register(
        EnvConfigLoaderArgs,
        lambda config_loader_args: EnvConfigLoader(
            config_provider=FileConfigProvider(file_path=config_loader_args.file_path),
            env_processor=DefaultEnvConfigProcessor(),
        ),
    )

    factory.register(
        JsonConfigLoaderArgs,
        lambda config_loader_args: JsonConfigLoader(config_provider=FileConfigProvider(file_path=config_loader_args.file_path)),
    )

    factory.register(
        YamlConfigLoaderArgs,
        lambda config_loader_args: YamlConfigLoader(config_provider=FileConfigProvider(file_path=config_loader_args.file_path)),
    )


def load_settings(factory: ConfigLoaderFactoryRegistry, config_loader_args: ConfigLoaderArgs, logger: logging.Logger) -> Settings:
    """
    Generic function to load settings based on provided arguments.
    """
    config_loader = factory.get_loader(config_loader_args=config_loader_args)
    logger.info(f"Loaded configuration using loader: {config_loader.__class__.__name__}")
    settings = Settings.load(config_loader=config_loader)
    return settings


class SettingsSource(TypedDict):
    config_loader_args: ConfigLoaderArgs  # The argument instance, e.g., GcpSecretEnvConfigLoaderArgs, EnvConfigLoaderArgs
    description: str


def main():
    configure_logging()

    logger = logging.getLogger(__name__)

    project_id = "nexum-dev-364711"

    # Initialize factory and register loaders
    factory = ConfigLoaderFactoryRegistry.default()

    register_loaders(factory)

    # Load settings from various sources
    settings_sources: list[SettingsSource] = [
        {
            "config_loader_args": GcpSecretEnvConfigLoaderArgs(secret_name="app-config-env", project_id=project_id),
            "description": "GCP Env Secret: app-config-env",
        },
        {
            "config_loader_args": GcpSecretJsonConfigLoaderArgs(secret_name="app-config-json", project_id=project_id),
            "description": "GCP JSON Secret: app-config-json",
        },
        {
            "config_loader_args": GcpSecretYamlConfigLoaderArgs(secret_name="app-config-yaml", project_id=project_id),
            "description": "GCP YAML Secret: app-config-yaml",
        },
        {
            "config_loader_args": GcpStorageEnvConfigLoaderArgs(
                bucket_name="app-config-boilerplate", blob_name=".env", project_id=project_id
            ),
            "description": "GCP Env Storage: app-config-env",
        },
        {
            "config_loader_args": GcpStorageJsonConfigLoaderArgs(
                bucket_name="app-config-boilerplate", blob_name="config.json", project_id=project_id
            ),
            "description": "GCP JSON Storage: app-config-json",
        },
        {
            "config_loader_args": GcpStorageYamlConfigLoaderArgs(
                bucket_name="app-config-boilerplate", blob_name="config.yaml", project_id=project_id
            ),
            "description": "GCP YAML Storage: app-config-yaml",
        },
        {"config_loader_args": EnvConfigLoaderArgs(file_path=".env"), "description": "ENV File: .env"},
        {"config_loader_args": EnvConfigLoaderArgs(file_path=".env.local"), "description": "ENV File: .env.local"},
        {"config_loader_args": YamlConfigLoaderArgs(file_path="config.yaml"), "description": "YAML File: config.yaml"},
        {
            "config_loader_args": YamlConfigLoaderArgs(file_path="config.local.yaml"),
            "description": "YAML File: config.local.yaml",
        },
        {"config_loader_args": JsonConfigLoaderArgs(file_path="config.json"), "description": "JSON File: config.json"},
        {
            "config_loader_args": JsonConfigLoaderArgs(file_path="config.local.json"),
            "description": "JSON File: config.local.json",
        },
    ]

    for settings_source in settings_sources:
        config_loader_args = settings_source["config_loader_args"]
        description = settings_source["description"]
        try:
            settings = load_settings(factory, config_loader_args, logger)
            logger.info(f"Settings from {description}: {settings}")
        except Exception as e:
            logger.error(f"Failed to load settings from {description}: {e}")


if __name__ == "__main__":
    main()
