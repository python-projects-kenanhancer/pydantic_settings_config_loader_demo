from logging import Logger

from config_loaders.config_loader_args import (
    GcpStorageYamlConfigLoaderArgs,
)
from config_loaders.config_loader_args.env_config_loader_args import EnvConfigLoaderArgs
from config_loaders.decorators import inject_settings_from_loader_args
from decorators import inject_logger
from schemas import SayHelloSettings, Settings


@inject_logger()
@inject_settings_from_loader_args(
    GcpStorageYamlConfigLoaderArgs(bucket_name="app-config-boilerplate", blob_name="config.yaml", project_id="nexum-dev-364711")
)
@inject_settings_from_loader_args(EnvConfigLoaderArgs(file_path=".env.say_hello"), param_name="say_hello_settings")
def test_multiple_settings(logger: Logger, say_hello_settings: SayHelloSettings, settings: Settings):
    logger.info(f"Settings from gcp storage yaml file: {settings}")


def main():

    test_multiple_settings()


if __name__ == "__main__":
    main()
