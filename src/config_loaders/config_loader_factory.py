from typing import overload

from config_loaders.loader_args import (
    EnvLoaderArgs,
    GcpLoaderJsonArgs,
    GcpLoaderYamlArgs,
    LoaderArgs,
    YamlLoaderArgs,
)

from .config_loader import ConfigLoader
from .env_file_loader import EnvFileLoader
from .gcp_secret_json_loader import GcpSecretJsonLoader
from .gcp_secret_yaml_loader import GcpSecretYamlLoader
from .yaml_file_loader import YamlFileLoader


class ConfigLoaderFactory:
    @overload
    @staticmethod
    def get_loader(args: GcpLoaderJsonArgs) -> GcpSecretJsonLoader: ...

    @overload
    @staticmethod
    def get_loader(args: GcpLoaderYamlArgs) -> GcpSecretYamlLoader: ...

    @overload
    @staticmethod
    def get_loader(args: YamlLoaderArgs) -> YamlFileLoader: ...

    @overload
    @staticmethod
    def get_loader(args: EnvLoaderArgs) -> EnvFileLoader: ...

    @staticmethod
    def get_loader(args: LoaderArgs) -> ConfigLoader:
        if isinstance(args, GcpLoaderJsonArgs):
            return GcpSecretJsonLoader(secret_name=args.secret_name, project_id=args.project_id)
        elif isinstance(args, GcpLoaderYamlArgs):
            return GcpSecretYamlLoader(secret_name=args.secret_name, project_id=args.project_id)
        elif isinstance(args, YamlLoaderArgs):
            return YamlFileLoader(file_path=args.file_path)
        elif isinstance(args, EnvLoaderArgs):
            return EnvFileLoader(file_path=args.file_path)
        else:
            raise ValueError(f"Unsupported loader arguments: {args}")
