from typing import Any, Callable, Type

from config_loaders import ConfigLoaderFactory, GcpStorageJsonConfigLoaderArgs

from ..base_inject_settings import TSettings, inject_settings


def load_settings_from_gcp_storage_json(
    *, bucket_name: str, blob_name: str, project_id: str, SettingsClass: Type[TSettings]
) -> TSettings:
    gcp_json_config_loader = ConfigLoaderFactory.get_loader(
        GcpStorageJsonConfigLoaderArgs(bucket_name=bucket_name, blob_name=blob_name, project_id=project_id)
    )
    return SettingsClass.load(config_loader=gcp_json_config_loader)


def inject_settings_from_gcp_storage_json(
    bucket_name: str, blob_name: str, project_id: str, SettingsClass: Type[TSettings]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return inject_settings(
        load_settings_from_gcp_storage_json, SettingsClass, bucket_name=bucket_name, blob_name=blob_name, project_id=project_id
    )
