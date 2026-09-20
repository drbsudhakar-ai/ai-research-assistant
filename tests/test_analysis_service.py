"""Application-service boundary tests for AnalysisService."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.core.pipeline.pipeline_context import PipelineContext
from app.core.pipeline.pipeline_keys import PipelineKeys
from app.core.pipeline.pipeline_result import PipelineResult
from app.models.analysis_request import AnalysisRequest
from app.models.analysis_result import AnalysisResult
from app.models.exceptions import AnalysisError
from app.services.analysis_service import AnalysisService

_SERVICE_PATH = Path("app/services/analysis_service.py")


def _request() -> AnalysisRequest:
    return AnalysisRequest(
        source_path="C:/tmp/paper.pdf",
        filename="paper.pdf",
    )


def _result() -> AnalysisResult:
    return AnalysisResult(
        analysis="findings",
        provider="ollama",
        model="qwen3:4b",
        execution_time=1.0,
    )


def test_analyze_accepts_request_and_returns_result() -> None:
    stored = _result()
    context = PipelineContext(data={PipelineKeys.ANALYSIS_RESULT: stored})
    pipeline_result = PipelineResult.success_result(context=context, execution_time=1.0)
    factory = Mock()
    factory.create.return_value = object()
    service = AnalysisService(pipeline_factory=factory)

    with patch("app.services.analysis_service.PipelineRunner") as runner_cls:
        runner_cls.return_value.run.return_value = pipeline_result
        outcome = service.analyze(_request())

    assert outcome is stored
    factory.create.assert_called_once()
    context_arg = runner_cls.return_value.run.call_args[0][0]
    assert context_arg.get(PipelineKeys.PDF_PATH) == "C:/tmp/paper.pdf"
    assert context_arg.get(PipelineKeys.FILENAME) == "paper.pdf"


def test_analyze_with_record_id_returns_persisted_identity() -> None:
    stored = _result()
    context = PipelineContext(
        data={
            PipelineKeys.ANALYSIS_RESULT: stored,
            PipelineKeys.HISTORY_RECORD_ID: 42,
        }
    )
    pipeline_result = PipelineResult.success_result(context=context, execution_time=1.0)
    service = AnalysisService(pipeline_factory=Mock())
    with patch("app.services.analysis_service.PipelineRunner") as runner_cls:
        runner_cls.return_value.run.return_value = pipeline_result
        result, record_id = service.analyze_with_record_id(_request())
    assert result is stored
    assert record_id == 42


def test_analyze_rejects_non_request() -> None:
    service = AnalysisService(pipeline_factory=Mock())
    with pytest.raises(AnalysisError, match="AnalysisRequest"):
        service.analyze("paper.pdf")  # type: ignore[arg-type]


def test_pipeline_failure_raises_application_error() -> None:
    context = PipelineContext()
    pipeline_result = PipelineResult.failure_result(
        context=context,
        error=RuntimeError("provider sdk exploded"),
        failed_step="Analyze Research Paper",
        execution_time=0.2,
    )
    factory = Mock()
    factory.create.return_value = object()
    service = AnalysisService(pipeline_factory=factory)

    with patch("app.services.analysis_service.PipelineRunner") as runner_cls:
        runner_cls.return_value.run.return_value = pipeline_result
        with pytest.raises(AnalysisError, match="Research paper analysis failed"):
            service.analyze(_request())


def test_missing_result_raises_application_error() -> None:
    context = PipelineContext()
    pipeline_result = PipelineResult.success_result(context=context, execution_time=0.1)
    factory = Mock()
    factory.create.return_value = object()
    service = AnalysisService(pipeline_factory=factory)

    with patch("app.services.analysis_service.PipelineRunner") as runner_cls:
        runner_cls.return_value.run.return_value = pipeline_result
        with pytest.raises(AnalysisError, match="without an AnalysisResult"):
            service.analyze(_request())


def test_history_repository_is_not_used_by_analysis_service() -> None:
    source = _SERVICE_PATH.read_text(encoding="utf-8")
    assert "HistoryRepository" not in source
    assert "sqlite3" not in source
    assert "from app.storage" not in source


def test_provider_objects_do_not_leak_from_analysis_service() -> None:
    source = _SERVICE_PATH.read_text(encoding="utf-8")
    assert "ollama" not in source.lower()
    assert "OllamaService" not in source
    assert "UploadedFile" not in source
    stored = _result()
    context = PipelineContext(data={PipelineKeys.ANALYSIS_RESULT: stored})
    pipeline_result = PipelineResult.success_result(context=context, execution_time=1.0)
    service = AnalysisService(pipeline_factory=Mock())
    mapped = service.result_from_pipeline(pipeline_result)
    assert type(mapped).__name__ == "AnalysisResult"


def test_analysis_service_has_no_streamlit_dependency() -> None:
    source = _SERVICE_PATH.read_text(encoding="utf-8")
    assert "streamlit" not in source
    assert "import st" not in source
