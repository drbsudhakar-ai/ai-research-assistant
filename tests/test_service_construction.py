"""Service construction tests (live composition root)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.core.pipeline import BasePipelineStep, ResearchAnalysisPipeline


def test_service_factory_delegates_to_container() -> None:
    source = Path("app/services/service_factory.py").read_text(encoding="utf-8")
    assert "ServiceContainer" in source
    assert "create_analysis_service" in source


def test_bootstrap_delegates_to_container() -> None:
    source = Path("app/bootstrap/analysis_container.py").read_text(encoding="utf-8")
    assert "ServiceContainer" in source
    assert "build_analysis_service" in source


def test_service_container_builds_analysis_service() -> None:
    pytest.importorskip("fitz")
    pytest.importorskip("ollama")
    from app.services.analysis_service import AnalysisService
    from app.services.service_container import ServiceContainer

    container = ServiceContainer()
    service = container.analysis_service
    assert isinstance(service, AnalysisService)
    pipeline = container.research_analysis_pipeline_factory.create()
    assert isinstance(pipeline, ResearchAnalysisPipeline)
    assert pipeline.step_count == 4
    assert all(isinstance(step, BasePipelineStep) for step in pipeline.steps)
    names = pipeline.names
    assert "Validate PDF" in names
    assert "Prepare Research Paper" in names
    assert "Analyze Research Paper" in names
    assert "Save Analysis History" in names


def test_service_factory_and_bootstrap_use_same_service_type() -> None:
    pytest.importorskip("fitz")
    pytest.importorskip("ollama")
    from app.bootstrap.analysis_container import build_analysis_service
    from app.services.analysis_service import AnalysisService
    from app.services.service_factory import ServiceFactory

    from_factory = ServiceFactory.create_analysis_service()
    from_bootstrap = build_analysis_service()
    assert isinstance(from_factory, AnalysisService)
    assert isinstance(from_bootstrap, AnalysisService)
