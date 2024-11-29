from typing import overload

from config_loaders.loader_args import (
    EnvLoaderArgs,
    GcpLoaderArgs,
    LoaderArgs,
    YamlLoaderArgs,
)

from .config_loader import ConfigLoader
from .env_file_loader import EnvFileLoader
from .gcp_secret_loader import GcpSecretLoader
from .yaml_file_loader import YamlFileLoader


class ConfigLoaderFactory:
    @overload
    @staticmethod
    def get_loader(args: GcpLoaderArgs) -> GcpSecretLoader: ...

    @overload
    @staticmethod
    def get_loader(args: YamlLoaderArgs) -> YamlFileLoader: ...

    @overload
    @staticmethod
    def get_loader(args: EnvLoaderArgs) -> EnvFileLoader: ...

    @staticmethod
    def get_loader(args: LoaderArgs) -> ConfigLoader:
        if isinstance(args, GcpLoaderArgs):
            return GcpSecretLoader(secret_name=args.secret_name, project_id=args.project_id)
        elif isinstance(args, YamlLoaderArgs):
            return YamlFileLoader(file_path=args.file_path)
        elif isinstance(args, EnvLoaderArgs):
            return EnvFileLoader(file_path=args.file_path)
        else:
            raise ValueError(f"Unsupported loader arguments: {args}")
