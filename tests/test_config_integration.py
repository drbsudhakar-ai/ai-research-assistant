"""Configuration integration with ServiceContainer and SQLite path."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.config.env_names import ENV_DATABASE_PATH, ENV_LLM_MODEL
from app.config.loader import load_application_config, reset_application_config
from app.storage.database import get_database_path, initialize_database


@pytest.fixture(autouse=True)
def _reset_config() -> None:
    reset_application_config()
    yield
    reset_application_config()


def test_database_initialize_uses_configured_path(tmp_path: Path) -> None:
    db_path = tmp_path / "history.db"
    load_application_config(
        environ={ENV_DATABASE_PATH: str(db_path)},
        load_dotenv=False,
        set_as_current=True,
    )
    assert get_database_path() == db_path
    initialize_database()
    assert db_path.is_file()


def test_service_container_uses_canonical_config() -> None:
    pytest.importorskip("fitz")
    pytest.importorskip("ollama")
    from app.services.service_container import ServiceContainer

    config = load_application_config(
        environ={ENV_LLM_MODEL: "configured-model"},
        load_dotenv=False,
        set_as_current=True,
    )
    container = ServiceContainer(config)
    assert container.config is config
    assert container.llm_service.model == "configured-model"


def test_service_container_propagates_developer_mode() -> None:
    pytest.importorskip("fitz")
    pytest.importorskip("ollama")
    from app.config.env_names import ENV_DEVELOPER_MODE
    from app.services.service_container import ServiceContainer

    config = load_application_config(
        environ={ENV_DEVELOPER_MODE: "true"},
        load_dotenv=False,
        set_as_current=True,
    )
    service = ServiceContainer(config).llm_service
    assert service._provider.developer_mode is True
    assert service._provider.base_url == config.llm.base_url
