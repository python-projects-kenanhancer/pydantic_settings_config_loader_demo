import pytest

from settings import Settings


class TestSettingsBasic:

    def test_settings_with_mock_environment_variables(self, monkeypatch: pytest.MonkeyPatch):
        # Mock Meta-Database environment variables
        monkeypatch.setenv("POSTGRES_USER", "airflow_test_user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "airflow_test_password")
        monkeypatch.setenv("POSTGRES_DB", "airflow_test_db")

        # Mock Backend DB environment variables
        monkeypatch.setenv(
            "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN",
            "postgresql+psycopg2://airflow:airflow@postgres/airflow",
        )
        monkeypatch.setenv("AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS", "False")

        # Mock Airflow Init environment variables
        monkeypatch.setenv("_AIRFLOW_DB_UPGRADE", "True")
        monkeypatch.setenv("_AIRFLOW_WWW_USER_CREATE", "True")
        monkeypatch.setenv("_AIRFLOW_WWW_USER_USERNAME", "airflow")
        monkeypatch.setenv("_AIRFLOW_WWW_USER_PASSWORD", "airflow")

        # Mock Airflow Core environment variables
        monkeypatch.setenv("AIRFLOW__CORE__FERNET_KEY", "")
        monkeypatch.setenv("AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION", "True")
        monkeypatch.setenv("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
        monkeypatch.setenv("AIRFLOW_UID", "0")

        # Mock CDT_TO_NEXUM environment variables
        monkeypatch.setenv("AIRFLOW_HOME", "$PWD")
        monkeypatch.setenv("GCP_PROJECT", "")
        monkeypatch.setenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            "$HOME/.config/gcloud/application_default_credentials.json",
        )
        monkeypatch.setenv("CDT_DATASET", "cdt_ovo_to_nexum")
        monkeypatch.setenv("PROJECT_ENV", "dev")
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "nexum-dev")
        monkeypatch.setenv("no_proxy", "*")
        monkeypatch.setenv("DATASET_OUTPUT_ENV", "$(git rev-parse --abbrev-ref HEAD)")
        monkeypatch.setenv("INTTEST_DSET", "integration_test")

        # Mock Feature Flags
        monkeypatch.setenv("SPLIT_BALANCES_ENABLED", "True")
        monkeypatch.setenv("CIRCUIT_BREAKER_ENABLED", "True")
        monkeypatch.setenv("CIRCUIT_BREAKER_CHECKS_SUBSET_CONFIG", "{}")
        monkeypatch.setenv("CIRCUIT_BREAKER_DURATION", 0)

        settings = Settings()

        # Perform your assertions
        assert settings.meta_database.postgres_user == "airflow_test_user"
        assert settings.meta_database.postgres_db == "airflow_test_db"
