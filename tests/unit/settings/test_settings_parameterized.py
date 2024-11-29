import pytest

from settings import Settings, load_environment_file


class TestSettingsParameterized:

    @pytest.fixture
    def env_suffix(self, request):
        return request.param

    @pytest.fixture
    def settings(self, env_suffix):

        load_environment_file(env_suffix)

        return Settings()

    @pytest.mark.parametrize(
        "env_suffix, expected_settings",
        [
            (
                "",
                {
                    "meta_database": {"postgres_user": "airflow", "postgres_db": "airflow"},
                    "airflow_core": {"airflow_uid": 55, "load_examples": False},
                    "feature_flags": {"circuit_breaker_enabled": True, "circuit_breaker_duration": 11},
                },
            ),
            (
                "dev",
                {
                    "meta_database": {"postgres_user": "airflowddddd", "postgres_db": "airflowwwww"},
                    "airflow_core": {"airflow_uid": 0, "load_examples": False},
                    "feature_flags": {"circuit_breaker_enabled": False, "circuit_breaker_duration": -3},
                },
            ),
            (
                "local",
                {
                    "meta_database": {"postgres_user": "KENAN", "postgres_db": "KENAN"},
                    "airflow_core": {"airflow_uid": 1000, "load_examples": True},
                    "feature_flags": {"circuit_breaker_enabled": True, "circuit_breaker_duration": 5},
                },
            ),
        ],
        indirect=["env_suffix"],  # Resolve the `settings` parameter via the fixture
    )
    def test_settings_with_different_environments(self, settings, expected_settings):

        for section, fields in expected_settings.items():
            for field, expected_value in fields.items():
                actual_value = getattr(getattr(settings, section), field)
                assert actual_value == expected_value
