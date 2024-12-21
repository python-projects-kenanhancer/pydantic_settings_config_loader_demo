from typing import Any, Callable, Type

from config_loaders import ConfigLoaderFactory, EnvConfigLoaderArgs

from .base_inject_settings import TSettings, inject_settings


def load_settings_from_env_file(*, file_path: str, SettingsClass: Type[TSettings]):
    env_config_loader = ConfigLoaderFactory.get_loader(EnvConfigLoaderArgs(file_path=file_path))

    return SettingsClass.load(config_loader=env_config_loader)


def inject_settings_from_env_file(
    file_path: str, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return inject_settings(load_settings_from_env_file, SettingsClass, file_path=file_path)