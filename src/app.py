from config_loaders import (
    ConfigLoaderFactory,
    EnvLoaderArgs,
    YamlLoaderArgs,
)
from config_loaders.loader_args.gcp_loader_json_args import GcpLoaderJsonArgs
from schemas import Settings

# Benefits of Implemented Patterns and Principles:
# - Extensibility:
#       New loaders can be added with minimal changes.
# - Maintainability:
#       Clear separation of responsibilities makes the code easier to maintain.
# - Reusability:
#       Components can be reused in different contexts.
# - Testability:
#       Isolated classes and clear interfaces facilitate unit testing.
# - Readability:
#       Organized structure and clear naming conventions improve understanding.


# Factory Method Pattern - Allows for easy addition of new loaders without modifying existing code.
# New loaders can be added without modifying existing code - Open/Closed Principle (OCP)
# The use of LoaderArgs and its subclasses (GcpLoaderArgs, YamlLoaderArgs, EnvLoaderArgs) encapsulates the parameters required to initialize different loaders - Parameter Object Pattern


def load_with_gcp_json_loader(secret_name: str, project_id: str):

    gcp_config_loader = ConfigLoaderFactory.get_loader(GcpLoaderJsonArgs(secret_name=secret_name, project_id=project_id))

    settings_from_gcp = Settings.load(gcp_config_loader)

    return settings_from_gcp


def load_with_yaml_config_loader(file_path: str):
    yaml_config_loader = ConfigLoaderFactory.get_loader(YamlLoaderArgs(file_path=file_path))

    settings_from_yaml_file = Settings.load(yaml_config_loader)

    return settings_from_yaml_file


def load_with_env_config_loader(file_path: str):
    env_config_loader = ConfigLoaderFactory.get_loader(EnvLoaderArgs(file_path=file_path))

    settings_from_env_file = Settings.load(env_config_loader)

    return settings_from_env_file


def main():

    project_id = "nexum-dev-364711"
    secret_name = "app-config-json"

    settings_from_gcp = load_with_gcp_json_loader(secret_name=secret_name, project_id=project_id)

    print(settings_from_gcp)

    settings_from_yaml_file = load_with_yaml_config_loader("config.yaml")

    print(settings_from_yaml_file)

    settings_from_yaml_local_file = load_with_yaml_config_loader("config.local.yaml")

    print(settings_from_yaml_local_file)

    settings_from_env_file = load_with_env_config_loader(".env")

    print(settings_from_env_file)

    settings_from_env_local_file = load_with_env_config_loader(".env.local")

    print(settings_from_env_local_file)


if __name__ == "__main__":
    main()
