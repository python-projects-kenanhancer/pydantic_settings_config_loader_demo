from dataclasses import dataclass

import pytest

from config_loaders import ConfigLoaderFactory, EnvLoaderArgs, JsonLoaderArgs, YamlLoaderArgs
from schemas import Settings


@dataclass
class UnifiedSettings:
    env: Settings | None = None
    json: Settings | None = None
    yaml: Settings | None = None


class TestSettingsWithLoadersAdvanced:

    @pytest.fixture
    def env_suffix(self, request):
        return request.param

    @pytest.fixture
    def settings(self, env_suffix):

        unified_settings = UnifiedSettings()

        if env_suffix:
            env_suffix = env_suffix.lower()
            env_file = f".env.{env_suffix}"
            json_file = f"config.{env_suffix}.json"
            yaml_file = f"config.{env_suffix}.yaml"

        else:
            env_file = ".env"
            json_file = "config.json"
            yaml_file = "config.yaml"

        settings_from_env_file = Settings.load(ConfigLoaderFactory.get_loader(EnvLoaderArgs(file_path=env_file)))
        settings_from_json_file = Settings.load(ConfigLoaderFactory.get_loader(JsonLoaderArgs(file_path=json_file)))
        settings_from_yaml_file = Settings.load(ConfigLoaderFactory.get_loader(YamlLoaderArgs(file_path=yaml_file)))

        unified_settings.env = settings_from_env_file
        unified_settings.json = settings_from_json_file
        unified_settings.yaml = settings_from_yaml_file

        return unified_settings

    @pytest.fixture
    def expected_settings(self, env_suffix):

        if env_suffix == "":
            return {
                "meta_database": {"postgres_user": "airflow", "postgres_db": "airflow"},
                "airflow_core": {"airflow_uid": 55, "load_examples": False},
                "feature_flags": {"circuit_breaker_enabled": True, "circuit_breaker_duration": 11},
            }
        elif env_suffix == "dev":
            return {
                "meta_database": {"postgres_user": "airflowddddd", "postgres_db": "airflowwwww"},
                "airflow_core": {"airflow_uid": 0, "load_examples": False},
                "feature_flags": {"circuit_breaker_enabled": False, "circuit_breaker_duration": -3},
            }
        elif env_suffix == "local":
            return {
                "meta_database": {"postgres_user": "KENAN", "postgres_db": "KENAN"},
                "airflow_core": {"airflow_uid": 1000, "load_examples": True},
                "feature_flags": {"circuit_breaker_enabled": True, "circuit_breaker_duration": 5},
            }
        else:
            raise ValueError(f"Unknown environment suffix: {env_suffix}")

    @pytest.mark.parametrize(
        "env_suffix",
        [
            "",
            "dev",
            "local",
        ],
        indirect=["env_suffix"],  # Resolve via the env_suffix fixture
    )
    def test_settings_with_different_environments(self, settings: UnifiedSettings, expected_settings):

        for section, fields in expected_settings.items():
            for field, expected_value in fields.items():
                actual_env_value = getattr(getattr(settings.env, section), field)
                actual_json_value = getattr(getattr(settings.json, section), field)
                actual_yaml_value = getattr(getattr(settings.yaml, section), field)
                assert actual_env_value == expected_value
                assert actual_json_value == expected_value
                assert actual_yaml_value == expected_value
