from typing import Any, Callable, Type

from config_loaders import ConfigLoaderFactory, GcpSecretYamlConfigLoaderArgs

from ..base_inject_settings import TSettings, inject_settings


def load_settings_from_gcp_secret_yaml(*, secret_name: str, project_id: str, SettingsClass: Type[TSettings]) -> TSettings:
    gcp_yaml_config_loader = ConfigLoaderFactory.get_loader(
        GcpSecretYamlConfigLoaderArgs(secret_name=secret_name, project_id=project_id)
    )
    return SettingsClass.load(config_loader=gcp_yaml_config_loader)


def inject_settings_from_gcp_secret_yaml(
    secret_name: str, project_id: str, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return inject_settings(load_settings_from_gcp_secret_yaml, SettingsClass, secret_name=secret_name, project_id=project_id)