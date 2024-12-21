from typing import Any, Callable, Protocol, Type, TypeVar

from typing_extensions import Self


class BaseSettings(Protocol):
    @classmethod
    def load(cls: Type[Self], config_loader: Any) -> Self: ...


TSettings = TypeVar("TSettings", bound=BaseSettings)


def inject_settings(
    loader_func: Callable[..., TSettings], SettingsClass: Type[TSettings], **loader_args: Any
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._settings = None

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if func._settings is None:
                settings_instance = loader_func(SettingsClass=SettingsClass, **loader_args)
                func._settings = settings_instance
            return func(*args, **kwargs, settings=func._settings)

        return wrapper

    return decorator


__all__ = ["BaseSettings", "TSettings", "inject_settings"]
