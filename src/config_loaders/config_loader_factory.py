from typing import overload

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

from .config_loader import ConfigLoader
from .config_providers import FileConfigProvider, GcpSecretConfigProvider, GcpStorageConfigProvider
from .env_config_loader import EnvConfigLoader
from .env_config_processors import DefaultEnvConfigProcessor
from .json_config_loader import JsonConfigLoader
from .yaml_config_loader import YamlConfigLoader


class ConfigLoaderFactory:
    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpSecretEnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpSecretJsonConfigLoaderArgs) -> JsonConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpSecretYamlConfigLoaderArgs) -> YamlConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpStorageEnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpStorageJsonConfigLoaderArgs) -> JsonConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpStorageYamlConfigLoaderArgs) -> YamlConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: EnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: JsonConfigLoaderArgs) -> JsonConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: YamlConfigLoaderArgs) -> YamlConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: ConfigLoaderArgs) -> ConfigLoader: ...

    @staticmethod
    def get_loader(config_loader_args: ConfigLoaderArgs) -> ConfigLoader:
        if isinstance(config_loader_args, GcpSecretEnvConfigLoaderArgs):
            config_provider = GcpSecretConfigProvider(
                secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
            )
            env_processor = DefaultEnvConfigProcessor()
            return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)
        elif isinstance(config_loader_args, GcpSecretJsonConfigLoaderArgs):
            config_provider = GcpSecretConfigProvider(
                secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
            )
            return JsonConfigLoader(config_provider=config_provider)
        elif isinstance(config_loader_args, GcpSecretYamlConfigLoaderArgs):
            config_provider = GcpSecretConfigProvider(
                secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
            )
            return YamlConfigLoader(config_provider=config_provider)
        elif isinstance(config_loader_args, GcpStorageEnvConfigLoaderArgs):
            config_provider = GcpStorageConfigProvider(
                bucket_name=config_loader_args.bucket_name,
                blob_name=config_loader_args.blob_name,
                project_id=config_loader_args.project_id,
            )
            env_processor = DefaultEnvConfigProcessor()
            return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)
        elif isinstance(config_loader_args, GcpStorageJsonConfigLoaderArgs):
            config_provider = GcpStorageConfigProvider(
                bucket_name=config_loader_args.bucket_name,
                blob_name=config_loader_args.blob_name,
                project_id=config_loader_args.project_id,
            )
            return JsonConfigLoader(config_provider=config_provider)
        elif isinstance(config_loader_args, GcpStorageYamlConfigLoaderArgs):
            config_provider = GcpStorageConfigProvider(
                bucket_name=config_loader_args.bucket_name,
                blob_name=config_loader_args.blob_name,
                project_id=config_loader_args.project_id,
            )
            return YamlConfigLoader(config_provider=config_provider)
        elif isinstance(config_loader_args, EnvConfigLoaderArgs):
            config_provider = FileConfigProvider(file_path=config_loader_args.file_path)
            env_processor = DefaultEnvConfigProcessor()
            return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)
        elif isinstance(config_loader_args, JsonConfigLoaderArgs):
            config_provider = FileConfigProvider(file_path=config_loader_args.file_path)
            return JsonConfigLoader(config_provider=config_provider)
        elif isinstance(config_loader_args, YamlConfigLoaderArgs):
            config_provider = FileConfigProvider(file_path=config_loader_args.file_path)
            return YamlConfigLoader(config_provider=config_provider)
        else:
            raise ValueError(f"Unsupported loader arguments: {config_loader_args}")
