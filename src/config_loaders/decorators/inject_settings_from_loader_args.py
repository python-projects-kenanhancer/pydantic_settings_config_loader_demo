from typing import Any, Callable, Type, overload

from config_loaders import ConfigLoaderFactory
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

from .base_inject_settings import TSettings, inject_settings


def load_settings_from_env_file(*, config_loader_args: ConfigLoaderArgs, SettingsClass: Type[TSettings]):
    env_config_loader = ConfigLoaderFactory.get_loader(config_loader_args=config_loader_args)

    return SettingsClass.load(config_loader=env_config_loader)


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpSecretEnvConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpSecretJsonConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpSecretYamlConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpStorageEnvConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpStorageJsonConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: GcpStorageYamlConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: EnvConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: JsonConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


@overload
def inject_settings_from_loader_args(
    config_loader_args: YamlConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...


def inject_settings_from_loader_args(
    config_loader_args: ConfigLoaderArgs, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return inject_settings(load_settings_from_env_file, SettingsClass, config_loader_args=config_loader_args)
