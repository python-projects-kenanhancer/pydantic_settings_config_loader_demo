from typing import overload

from config_loaders.loader_args import (
    EnvLoaderArgs,
    GcpLoaderEnvArgs,
    GcpLoaderJsonArgs,
    GcpLoaderYamlArgs,
    JsonLoaderArgs,
    LoaderArgs,
    YamlLoaderArgs,
)

from .config_loader import ConfigLoader
from .config_providers import FileConfigProvider, GcpSecretConfigProvider
from .env_loader import EnvLoader
from .env_processors import DefaultEnvProcessor
from .json_loader import JsonLoader
from .yaml_loader import YamlLoader


class ConfigLoaderFactory:
    @overload
    @staticmethod
    def get_loader(args: GcpLoaderEnvArgs) -> EnvLoader: ...

    @overload
    @staticmethod
    def get_loader(args: GcpLoaderJsonArgs) -> JsonLoader: ...

    @overload
    @staticmethod
    def get_loader(args: GcpLoaderYamlArgs) -> YamlLoader: ...

    @overload
    @staticmethod
    def get_loader(args: EnvLoaderArgs) -> EnvLoader: ...

    @overload
    @staticmethod
    def get_loader(args: JsonLoaderArgs) -> JsonLoader: ...

    @overload
    @staticmethod
    def get_loader(args: YamlLoaderArgs) -> YamlLoader: ...

    @staticmethod
    def get_loader(args: LoaderArgs) -> ConfigLoader:
        if isinstance(args, GcpLoaderEnvArgs):
            config_provider = GcpSecretConfigProvider(secret_name=args.secret_name, project_id=args.project_id)
            env_processor = DefaultEnvProcessor()
            return EnvLoader(config_provider=config_provider, env_processor=env_processor)
        elif isinstance(args, GcpLoaderJsonArgs):
            config_provider = GcpSecretConfigProvider(secret_name=args.secret_name, project_id=args.project_id)
            return JsonLoader(config_provider=config_provider)
        elif isinstance(args, GcpLoaderYamlArgs):
            config_provider = GcpSecretConfigProvider(secret_name=args.secret_name, project_id=args.project_id)
            return YamlLoader(config_provider=config_provider)
        elif isinstance(args, EnvLoaderArgs):
            config_provider = FileConfigProvider(file_path=args.file_path)
            env_processor = DefaultEnvProcessor()
            return EnvLoader(config_provider=config_provider, env_processor=env_processor)
        elif isinstance(args, JsonLoaderArgs):
            config_provider = FileConfigProvider(file_path=args.file_path)
            return JsonLoader(config_provider=config_provider)
        elif isinstance(args, YamlLoaderArgs):
            config_provider = FileConfigProvider(file_path=args.file_path)
            return YamlLoader(config_provider=config_provider)
        else:
            raise ValueError(f"Unsupported loader arguments: {args}")
