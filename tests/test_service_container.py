"""Composition-root tests for ServiceContainer."""

from __future__ import annotations

from pathlib import Path

import pytest

_CONTAINER_PATH = Path("app/services/service_container.py")
_FACTORY_PATH = Path("app/services/service_factory.py")
_BOOTSTRAP_PATH = Path("app/bootstrap/analysis_container.py")


def test_container_source_uses_application_config() -> None:
    source = _CONTAINER_PATH.read_text(encoding="utf-8")
    assert "ApplicationConfig" in source
    assert "get_application_config" in source
    assert "LLMService.from_config" in source
    assert "import os" not in source
    assert "load_dotenv" not in source


def test_container_and_analysis_service_have_no_streamlit() -> None:
    container_source = _CONTAINER_PATH.read_text(encoding="utf-8")
    service_source = Path("app/services/analysis_service.py").read_text(
        encoding="utf-8"
    )
    assert "streamlit" not in container_source
    assert "streamlit" not in service_source


def test_history_is_wired_through_history_service() -> None:
    source = _CONTAINER_PATH.read_text(encoding="utf-8")
    assert "HistoryService" in source
    assert "history_service=self.history_service" in source
    assert "HistoryRepository" in source
    service_source = Path("app/services/analysis_service.py").read_text(
        encoding="utf-8"
    )
    assert "HistoryRepository" not in service_source


def test_compatibility_modules_delegate_to_container() -> None:
    factory = _FACTORY_PATH.read_text(encoding="utf-8")
    bootstrap = _BOOTSTRAP_PATH.read_text(encoding="utf-8")
    assert "ServiceContainer().analysis_service" in factory
    assert "ServiceContainer().analysis_service" in bootstrap
    assert "PipelineRunner" not in factory
    assert "PipelineRunner" not in bootstrap
    assert "PaperAnalyzer" not in factory
    assert "PaperAnalyzer" not in bootstrap


def test_container_receives_application_config() -> None:
    pytest.importorskip("fitz")
    pytest.importorskip("ollama")
    from app.config.application_config import (
        ApplicationConfig,
        default_application_config,
    )
    from app.services.service_container import ServiceContainer

    config = default_application_config()
    container = ServiceContainer(config)
    assert container.config is config
    assert isinstance(container.config, ApplicationConfig)


def test_container_builds_injected_analysis_service() -> None:
    pytest.importorskip("fitz")
    pytest.importorskip("ollama")
    from app.config.application_config import default_application_config
    from app.services.analysis_service import AnalysisService
    from app.services.history_service import HistoryService
    from app.services.service_container import ServiceContainer
    from app.storage.history_repository import HistoryRepository

    container = ServiceContainer(default_application_config())
    assert isinstance(container.analysis_service, AnalysisService)
    assert isinstance(container.history_service, HistoryService)
    assert isinstance(container.history_repository, HistoryRepository)
