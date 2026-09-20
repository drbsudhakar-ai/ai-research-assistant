"""Domain contract construction, validation, and compatibility tests."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.core.analysis.analysis_status import AnalysisStatus as CompatStatus
from app.core.pipeline.pipeline_keys import PipelineKeys
from app.core.progress.progress_event import ProgressEvent
from app.core.progress.progress_stage import ProgressStage
from app.models import (
    AnalysisRecord,
    AnalysisRequest,
    AnalysisResult,
    AnalysisStatus,
    LLMResponse,
    PaperSections,
    PreparedPaper,
)
from app.models.exceptions import DomainValidationError
from app.reports.report_document import ReportDocument


def _sample_sections() -> PaperSections:
    return PaperSections(abstract="An abstract.", introduction="Intro.")


def _sample_paper() -> PreparedPaper:
    return PreparedPaper(
        title="A Study",
        title_source="filename",
        title_confidence=0.8,
        filename="paper.pdf",
        text="body",
        total_pages=2,
        total_characters=4,
        sections=_sample_sections(),
    )


def test_models_package_does_not_import_streamlit_or_sqlite() -> None:
    models_dir = Path("app/models")
    forbidden = ("streamlit", "sqlite3", "ollama")
    for path in models_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".", 1)[0] for alias in node.names]
                assert not any(name in forbidden for name in names), path
            if isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                assert root not in forbidden, path


def test_paper_sections_empty_and_count_api() -> None:
    empty = PaperSections()
    assert empty.section_count == 0
    assert empty.is_empty
    assert len(empty) == empty.section_count
    sections = _sample_sections()
    assert sections.section_count == 2
    assert "Abstract" in sections.available_sections
    round_trip = PaperSections.from_dict(sections.to_dict())
    assert round_trip.abstract == "An abstract."


def test_paper_sections_reject_non_string() -> None:
    with pytest.raises(DomainValidationError):
        PaperSections(abstract=123)  # type: ignore[arg-type]


def test_prepared_paper_round_trip_and_validation() -> None:
    paper = _sample_paper()
    restored = PreparedPaper.from_dict(paper.to_dict())
    assert restored.title == "A Study"
    assert restored.sections.section_count == 2
    with pytest.raises(DomainValidationError):
        PreparedPaper(
            title="A Study",
            title_source="filename",
            title_confidence=0.8,
            filename="paper.pdf",
            text="body",
            total_pages=-1,
            total_characters=4,
            sections=_sample_sections(),
        )


def test_analysis_request_rejects_blank_path() -> None:
    request = AnalysisRequest(source_path="data/uploads/paper.pdf")
    assert request.filename == "paper.pdf"
    with pytest.raises(DomainValidationError):
        AnalysisRequest(source_path="   ")


def test_analysis_request_has_no_uploaded_file_field() -> None:
    assert "uploaded_file" not in AnalysisRequest.__dataclass_fields__


def test_llm_response_is_provider_neutral() -> None:
    response = LLMResponse(content="ok", provider="ollama", model="qwen3:4b")
    assert response.to_dict()["provider"] == "ollama"
    with pytest.raises(DomainValidationError):
        LLMResponse(content="ok", provider="", model="qwen3:4b")


def test_analysis_result_from_llm_and_record() -> None:
    response = LLMResponse(content="findings", provider="ollama", model="qwen3:4b")
    result = AnalysisResult.from_llm_response(response, execution_time=1.5)
    assert result.analysis == "findings"
    record = AnalysisRecord.from_result(result, paper=_sample_paper())
    assert record.title == "A Study"
    assert record.to_result().provider == "ollama"
    restored = AnalysisResult.from_dict(result.to_dict())
    assert restored.status is AnalysisStatus.COMPLETED


def test_analysis_result_extracts_proposal_intelligence() -> None:
    response = LLMResponse(
        content=(
            "## 14. PROPOSAL INTELLIGENCE\n\n"
            "### Main Research Gap\n\nA verified methodological gap.\n\n"
            "### Future Scope\n\n1. Evaluate the proposed method.\n\n"
            "### Evidence Basis\n\nSupported by the limitations section."
        ),
        provider="gemini",
        model="gemini-test",
    )
    result = AnalysisResult.from_llm_response(response)
    assert result.research_gap == "A verified methodological gap."
    assert result.future_scope == "1. Evaluate the proposed method."

    record = AnalysisRecord.from_result(result, paper=_sample_paper())
    assert record.research_gap == result.research_gap
    assert record.future_scope == result.future_scope


def test_analysis_result_rejects_empty_content() -> None:
    with pytest.raises(DomainValidationError):
        AnalysisResult(analysis="  ", provider="ollama", model="qwen3:4b")


def test_analysis_status_cancel_states_are_distinct() -> None:
    assert AnalysisStatus.CANCEL_REQUESTED is not AnalysisStatus.CANCELLED
    assert AnalysisStatus.CANCEL_REQUESTED.is_active
    assert not AnalysisStatus.CANCEL_REQUESTED.is_finished
    assert AnalysisStatus.CANCELLED.is_finished
    assert not AnalysisStatus.CANCELLED.is_active
    assert CompatStatus is AnalysisStatus


def test_progress_event_is_ui_independent_and_validates_percentage() -> None:
    event = ProgressEvent(
        stage=ProgressStage.ANALYZING,
        message="working",
        percentage=40,
    )
    payload = event.to_dict()
    assert payload["stage"] == "ANALYZING"
    assert "streamlit" not in payload
    with pytest.raises(DomainValidationError):
        ProgressEvent(stage=ProgressStage.ANALYZING, message="x", percentage=101)


def test_pipeline_keys_cover_live_context() -> None:
    assert PipelineKeys.PREPARED_PAPER == "prepared_paper"
    assert PipelineKeys.ANALYSIS_RESULT == "analysis_result"
    assert PipelineKeys.PDF_PATH == "pdf_path"


def test_report_document_does_not_render() -> None:
    result = AnalysisResult(
        analysis="body",
        provider="ollama",
        model="qwen3:4b",
    )
    document = ReportDocument.from_result(result, title="A Study")
    assert document.analysis == "body"
    assert document.paper_title == "A Study"


def test_history_record_round_trip() -> None:
    record = AnalysisRecord(title="A", analysis="B", provider="ollama", model="m")
    restored = AnalysisRecord.from_dict(record.to_dict())
    assert restored.title == "A"
    with pytest.raises(DomainValidationError):
        AnalysisRecord(total_pages=-2)


def test_analysis_service_reads_canonical_result_from_pipeline() -> None:
    pytest.importorskip("fitz")
    from unittest.mock import Mock

    from app.core.pipeline.pipeline_context import PipelineContext
    from app.core.pipeline.pipeline_result import PipelineResult
    from app.services.analysis_service import AnalysisService

    service = AnalysisService(pipeline_factory=Mock())
    stored = AnalysisResult(
        analysis="findings",
        provider="ollama",
        model="qwen3:4b",
    )
    context = PipelineContext(data={PipelineKeys.ANALYSIS_RESULT: stored})
    pipeline_result = PipelineResult.success_result(context=context, execution_time=1.0)
    result = service.result_from_pipeline(pipeline_result)
    assert result is stored


def test_analysis_service_rejects_history_record_as_pipeline_result() -> None:
    pytest.importorskip("fitz")
    from unittest.mock import Mock

    from app.core.pipeline.pipeline_context import PipelineContext
    from app.core.pipeline.pipeline_result import PipelineResult
    from app.services.analysis_service import AnalysisService

    service = AnalysisService(pipeline_factory=Mock())
    record = AnalysisRecord(analysis="findings", provider="ollama", model="qwen3:4b")
    context = PipelineContext(data={PipelineKeys.ANALYSIS_RESULT: record})
    pipeline_result = PipelineResult.success_result(context=context, execution_time=1.0)
    with pytest.raises(TypeError, match="AnalysisResult"):
        service.result_from_pipeline(pipeline_result)


def test_paper_analyzer_live_return_contract() -> None:
    source = Path("app/agents/paper_analyzer.py").read_text(encoding="utf-8")
    assert "def analyze(" in source
    assert "-> AnalysisResult" in source
    assert "AnalysisResult.from_llm_response" in source
    assert "return AnalysisRecord(" not in source
    assert "from app.models.analysis_record import AnalysisRecord" not in source


def test_save_history_step_converts_result_to_record() -> None:
    from unittest.mock import Mock

    from app.core.pipeline.pipeline_context import PipelineContext
    from app.pipeline.steps.save_history_step import SaveHistoryStep

    result = AnalysisResult(
        analysis="findings",
        provider="ollama",
        model="qwen3:4b",
        execution_time=1.25,
    )
    paper = _sample_paper()
    history = Mock()
    history.save_analysis.return_value = 42
    step = SaveHistoryStep(history_service=history)
    context = PipelineContext(
        data={
            PipelineKeys.ANALYSIS_RESULT: result,
            PipelineKeys.PREPARED_PAPER: paper,
            PipelineKeys.PAPER_METADATA: {
                "title": paper.title,
                "filename": paper.filename,
                "pages": paper.total_pages,
                "characters": paper.total_characters,
            },
        }
    )
    step.execute(context)
    history.save_analysis.assert_called_once()
    record = history.save_analysis.call_args[0][0]
    assert isinstance(record, AnalysisRecord)
    assert record.analysis == "findings"
    assert record.provider == "ollama"
    assert record.title == "A Study"
    assert context.data[PipelineKeys.HISTORY_RECORD_ID] == 42


def test_history_service_save_result_builds_record() -> None:
    from unittest.mock import Mock

    from app.services.history_service import HistoryService

    repository = Mock()
    repository.add.return_value = 7
    service = HistoryService(repository=repository)
    result = AnalysisResult(
        analysis="findings",
        provider="ollama",
        model="qwen3:4b",
    )
    record_id = service.save_result(result, paper=_sample_paper())
    assert record_id == 7
    saved = repository.add.call_args[0][0]
    assert isinstance(saved, AnalysisRecord)
    assert saved.analysis == "findings"
    assert saved.title == "A Study"
