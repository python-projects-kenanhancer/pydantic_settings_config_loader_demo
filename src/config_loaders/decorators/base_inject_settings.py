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
        # We store the loaded settings as an attribute on the function object
        func._settings = None

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # If 'settings' wasn't provided by the caller, inject it
            if "settings" not in kwargs:
                if func._settings is None:
                    settings_instance = loader_func(SettingsClass=SettingsClass, **loader_args)
                    func._settings = settings_instance
                kwargs["settings"] = func._settings

            # Now call the original function,
            # passing either the user-supplied settings or our loaded one.
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["BaseSettings", "TSettings", "inject_settings"]
