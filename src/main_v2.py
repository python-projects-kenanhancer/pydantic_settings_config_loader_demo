import logging
from typing import TypedDict

from config_loaders import (
    ConfigLoaderFactoryV2,
    DefaultEnvProcessor,
    EnvLoader,
    EnvLoaderArgs,
    FileConfigProvider,
    GcpLoaderEnvArgs,
    GcpLoaderJsonArgs,
    GcpLoaderYamlArgs,
    GcpSecretConfigProvider,
    JsonLoader,
    JsonLoaderArgs,
    LoaderArgs,
    YamlLoader,
    YamlLoaderArgs,
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


def register_loaders(factory: ConfigLoaderFactoryV2) -> None:
    """
    Register all necessary loaders with the factory.
    """
    factory.register(
        GcpLoaderEnvArgs,
        lambda args: EnvLoader(
            config_provider=GcpSecretConfigProvider(secret_name=args.secret_name, project_id=args.project_id),
            env_processor=DefaultEnvProcessor(),
        ),
    )

    factory.register(
        GcpLoaderJsonArgs,
        lambda args: JsonLoader(
            config_provider=GcpSecretConfigProvider(secret_name=args.secret_name, project_id=args.project_id)
        ),
    )

    factory.register(
        GcpLoaderYamlArgs,
        lambda args: YamlLoader(
            config_provider=GcpSecretConfigProvider(secret_name=args.secret_name, project_id=args.project_id)
        ),
    )

    factory.register(
        EnvLoaderArgs,
        lambda args: EnvLoader(
            config_provider=FileConfigProvider(file_path=args.file_path),
            env_processor=DefaultEnvProcessor(),
        ),
    )

    factory.register(
        JsonLoaderArgs,
        lambda args: JsonLoader(config_provider=FileConfigProvider(file_path=args.file_path)),
    )

    factory.register(
        YamlLoaderArgs,
        lambda args: YamlLoader(config_provider=FileConfigProvider(file_path=args.file_path)),
    )


def load_settings(factory: ConfigLoaderFactoryV2, args, logger: logging.Logger) -> Settings:
    """
    Generic function to load settings based on provided arguments.
    """
    config_loader = factory.get_loader(args=args)
    logger.info(f"Loaded configuration using loader: {config_loader.__class__.__name__}")
    settings = Settings.load(config_loader=config_loader)
    return settings


class SettingsSource(TypedDict):
    args: LoaderArgs  # The argument instance, e.g., GcpLoaderEnvArgs, EnvLoaderArgs
    description: str


def main():
    configure_logging()

    logger = logging.getLogger(__name__)

    project_id = "nexum-dev-364711"

    # Initialize factory and register loaders
    factory = ConfigLoaderFactoryV2.default()

    register_loaders(factory)

    # Load settings from various sources
    settings_sources: list[SettingsSource] = [
        {
            "args": GcpLoaderEnvArgs(secret_name="app-config-env", project_id=project_id),
            "description": "GCP Env Secret: app-config-env",
        },
        {
            "args": GcpLoaderJsonArgs(secret_name="app-config-json", project_id=project_id),
            "description": "GCP JSON Secret: app-config-json",
        },
        {
            "args": GcpLoaderYamlArgs(secret_name="app-config-yaml", project_id=project_id),
            "description": "GCP YAML Secret: app-config-yaml",
        },
        {"args": EnvLoaderArgs(file_path=".env"), "description": "ENV File: .env"},
        {"args": EnvLoaderArgs(file_path=".env.local"), "description": "ENV File: .env.local"},
        {"args": YamlLoaderArgs(file_path="config.yaml"), "description": "YAML File: config.yaml"},
        {"args": YamlLoaderArgs(file_path="config.local.yaml"), "description": "YAML File: config.local.yaml"},
        {"args": JsonLoaderArgs(file_path="config.json"), "description": "JSON File: config.json"},
        {"args": JsonLoaderArgs(file_path="config.local.json"), "description": "JSON File: config.local.json"},
    ]

    for settings_source in settings_sources:
        args = settings_source["args"]
        description = settings_source["description"]
        try:
            settings = load_settings(factory, args, logger)
            logger.info(f"Settings from {description}: {settings}")
        except Exception as e:
            logger.error(f"Failed to load settings from {description}: {e}")


if __name__ == "__main__":
    main()
