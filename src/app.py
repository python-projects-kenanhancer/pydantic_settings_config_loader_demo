from config_loaders import ConfigLoaderFactory
from config_loaders.loader_args import EnvLoaderArgs, GcpLoaderArgs, YamlLoaderArgs
from settings import Settings

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


def main():
    project_id = "nexum-dev-364711"
    secret_name = "app-config-json"

    gcp_config_loader = ConfigLoaderFactory.get_loader(GcpLoaderArgs(secret_name=secret_name, project_id=project_id))

    yaml_config_loader = ConfigLoaderFactory.get_loader(YamlLoaderArgs(file_path="config.yaml"))

    yaml_local_config_loader = ConfigLoaderFactory.get_loader(YamlLoaderArgs(file_path="config.local.yaml"))

    env_config_loader = ConfigLoaderFactory.get_loader(EnvLoaderArgs(file_path=".env"))

    env_local_config_loader = ConfigLoaderFactory.get_loader(EnvLoaderArgs(file_path=".env.local"))

    settings_from_gcp = Settings.load(gcp_config_loader)

    print(settings_from_gcp)

    settings_from_yaml_file = Settings.load(yaml_config_loader)

    print(settings_from_yaml_file)

    settings_from_yaml_local_file = Settings.load(yaml_local_config_loader)

    print(settings_from_yaml_local_file)

    settings_from_env_file = Settings.load(env_config_loader)

    print(settings_from_env_file)

    settings_from_env_local_file = Settings.load(env_local_config_loader)

    print(settings_from_env_local_file)


if __name__ == "__main__":
    main()
