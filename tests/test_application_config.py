"""Application configuration loading and validation tests."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from app.config.application_config import (
    SECRET_MASK,
    default_application_config,
    validate_application_config,
)
from app.config.env_names import (
    ENV_DATA_DIR,
    ENV_DATABASE_PATH,
    ENV_DEVELOPER_MODE,
    ENV_ENVIRONMENT,
    ENV_LLM_API_KEY,
    ENV_LLM_MODEL,
    ENV_LLM_PROVIDER,
    ENV_LLM_TEMPERATURE,
    ENV_LOG_LEVEL,
)
from app.config.exceptions import ConfigurationError
from app.config.loader import (
    configure_logging,
    get_application_config,
    load_application_config,
    reset_application_config,
)


@pytest.fixture(autouse=True)
def _reset_config() -> None:
    reset_application_config()
    yield
    reset_application_config()


def test_defaults_match_live_application() -> None:
    config = default_application_config()
    assert config.application.name == "AI Research Assistant"
    assert config.application.developer_mode is False
    assert config.llm.provider == "ollama"
    assert config.llm.model == "qwen3:4b"
    assert config.llm.base_url == "http://localhost:11434"
    assert config.llm.temperature == 0.2
    assert config.database.engine == "sqlite"
    assert config.database.path.name == "history.db"
    assert config.export.default_format == "markdown"
    assert config.export.pdf_enabled is False
    assert config.export.docx_enabled is False


def test_environment_overrides_defaults() -> None:
    config = load_application_config(
        environ={
            ENV_LLM_MODEL: "llama3.2:3b",
            ENV_LLM_TEMPERATURE: "0.1",
            ENV_ENVIRONMENT: "test",
            ENV_DEVELOPER_MODE: "true",
            ENV_LOG_LEVEL: "debug",
        },
        load_dotenv=False,
        set_as_current=False,
    )
    assert config.llm.model == "llama3.2:3b"
    assert config.llm.temperature == 0.1
    assert config.application.environment.value == "test"
    assert config.application.developer_mode is True
    assert config.logging.level == "DEBUG"


def test_explicit_overrides_beat_environment() -> None:
    config = load_application_config(
        environ={ENV_LLM_MODEL: "from-env"},
        overrides={"llm": {"model": "from-overrides"}},
        load_dotenv=False,
        set_as_current=False,
    )
    assert config.llm.model == "from-overrides"


def test_data_dir_relocates_default_database(tmp_path: Path) -> None:
    config = load_application_config(
        environ={ENV_DATA_DIR: str(tmp_path / "workspace")},
        load_dotenv=False,
        set_as_current=False,
    )
    assert config.paths.data_dir == tmp_path / "workspace"
    assert config.database.path == tmp_path / "workspace" / "history.db"
    assert config.paths.uploads_dir == tmp_path / "workspace" / "uploads"


def test_database_path_env_wins_over_data_dir(tmp_path: Path) -> None:
    db_path = tmp_path / "custom.db"
    config = load_application_config(
        environ={
            ENV_DATA_DIR: str(tmp_path / "workspace"),
            ENV_DATABASE_PATH: str(db_path),
        },
        load_dotenv=False,
        set_as_current=False,
    )
    assert config.database.path == db_path


def test_relative_paths_resolve_against_project_root() -> None:
    config = load_application_config(
        environ={ENV_DATABASE_PATH: "data/custom-history.db"},
        load_dotenv=False,
        set_as_current=False,
    )
    assert config.database.path.is_absolute()
    assert config.database.path.name == "custom-history.db"


def test_invalid_provider_fails_early() -> None:
    with pytest.raises(ConfigurationError, match="Unsupported runtime LLM provider"):
        load_application_config(
            environ={ENV_LLM_PROVIDER: "openai"},
            load_dotenv=False,
            set_as_current=False,
        )


def test_missing_model_fails_early() -> None:
    with pytest.raises(ConfigurationError, match="model name is required"):
        load_application_config(
            environ={ENV_LLM_MODEL: "   "},
            load_dotenv=False,
            set_as_current=False,
        )


def test_invalid_temperature_fails_early() -> None:
    with pytest.raises(ConfigurationError, match="Temperature"):
        load_application_config(
            environ={ENV_LLM_TEMPERATURE: "9"},
            load_dotenv=False,
            set_as_current=False,
        )


def test_invalid_boolean_fails_early() -> None:
    with pytest.raises(ConfigurationError, match="Invalid boolean"):
        load_application_config(
            environ={ENV_DEVELOPER_MODE: "maybe"},
            load_dotenv=False,
            set_as_current=False,
        )


def test_invalid_url_fails_early() -> None:
    with pytest.raises(ConfigurationError, match="Invalid URL"):
        load_application_config(
            overrides={"llm": {"base_url": "localhost:11434"}},
            load_dotenv=False,
            set_as_current=False,
        )


def test_get_application_config_caches_until_reset() -> None:
    first = load_application_config(
        environ={ENV_LLM_MODEL: "cached-model"},
        load_dotenv=False,
        set_as_current=True,
    )
    assert get_application_config() is first
    reset_application_config()
    second = load_application_config(environ={}, load_dotenv=False, set_as_current=True)
    assert second.llm.model == "qwen3:4b"


def test_safe_dict_redacts_api_key() -> None:
    config = load_application_config(
        environ={ENV_LLM_API_KEY: "sk-secret-value"},
        load_dotenv=False,
        set_as_current=False,
    )
    safe = config.to_safe_dict()
    dumped = str(safe)
    assert "sk-secret-value" not in dumped
    assert safe["llm"]["api_key"] == SECRET_MASK


def test_configure_logging_does_not_emit_secrets(
    caplog: pytest.LogCaptureFixture,
) -> None:
    config = load_application_config(
        environ={
            ENV_LLM_API_KEY: "sk-secret-value",
            ENV_LOG_LEVEL: "DEBUG",
        },
        load_dotenv=False,
        set_as_current=False,
    )
    with caplog.at_level(logging.DEBUG, logger="app.config.loader"):
        configure_logging(config)
    assert "sk-secret-value" not in caplog.text


def test_validate_rejects_non_sqlite_engine() -> None:
    config = default_application_config()
    with pytest.raises(ConfigurationError, match="database engine"):
        validate_application_config(
            config.__class__(
                application=config.application,
                llm=config.llm,
                database=config.database.__class__(
                    engine="postgres", path=config.database.path
                ),
                paths=config.paths,
                export=config.export,
                logging=config.logging,
                brand=config.brand,
            )
        )
