from config_loaders import (
    ConfigLoaderFactory,
    EnvLoaderArgs,
    GcpLoaderEnvArgs,
    GcpLoaderJsonArgs,
    GcpLoaderYamlArgs,
    JsonLoaderArgs,
    YamlLoaderArgs,
)
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


def load_settings_from_gcp_env(secret_name: str, project_id: str):

    gcp_env_config_loader = ConfigLoaderFactory.get_loader(GcpLoaderEnvArgs(secret_name=secret_name, project_id=project_id))

    settings = Settings.load(config_loader=gcp_env_config_loader)

    return settings


def load_settings_from_gcp_json(secret_name: str, project_id: str):

    gcp_json_config_loader = ConfigLoaderFactory.get_loader(GcpLoaderJsonArgs(secret_name=secret_name, project_id=project_id))

    settings = Settings.load(config_loader=gcp_json_config_loader)

    return settings


def load_settings_from_gcp_yaml(secret_name: str, project_id: str):

    gcp_yaml_config_loader = ConfigLoaderFactory.get_loader(GcpLoaderYamlArgs(secret_name=secret_name, project_id=project_id))

    settings = Settings.load(config_loader=gcp_yaml_config_loader)

    return settings


def load_settings_from_env_file(file_path: str):
    env_config_loader = ConfigLoaderFactory.get_loader(EnvLoaderArgs(file_path=file_path))

    settings = Settings.load(env_config_loader)

    return settings


def load_settings_from_json_file(file_path: str):
    json_config_loader = ConfigLoaderFactory.get_loader(JsonLoaderArgs(file_path=file_path))

    settings = Settings.load(json_config_loader)

    return settings


def load_settings_from_yaml_file(file_path: str):
    yaml_config_loader = ConfigLoaderFactory.get_loader(YamlLoaderArgs(file_path=file_path))

    settings = Settings.load(yaml_config_loader)

    return settings


def main():

    project_id = "nexum-dev-364711"

    settings_from_gcp_env = load_settings_from_gcp_env(secret_name="app-config-env", project_id=project_id)

    print(settings_from_gcp_env)

    settings_from_gcp_json = load_settings_from_gcp_json(secret_name="app-config-json", project_id=project_id)

    print(settings_from_gcp_json)

    settings_from_gcp_yaml = load_settings_from_gcp_yaml(secret_name="app-config-yaml", project_id=project_id)

    print(settings_from_gcp_yaml)

    settings_from_env_file = load_settings_from_env_file(".env")

    print(settings_from_env_file)

    settings_from_env_local_file = load_settings_from_env_file(".env.local")

    print(settings_from_env_local_file)

    settings_from_yaml_file = load_settings_from_yaml_file("config.yaml")

    print(settings_from_yaml_file)

    settings_from_yaml_local_file = load_settings_from_yaml_file("config.local.yaml")

    print(settings_from_yaml_local_file)


if __name__ == "__main__":
    main()
