"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Service
File         : analysis_service.py
Version      : 4.0.0

Description:
    Canonical application service for the research-paper analysis use case.

    Public contract:
        AnalysisRequest -> AnalysisResult

    Pipeline execution, history persistence, and provider calls remain
    behind this boundary.
===============================================================================
"""

from __future__ import annotations

from typing import Any, Protocol

from app.core.pipeline.pipeline_context import PipelineContext
from app.core.pipeline.pipeline_keys import PipelineKeys
from app.core.pipeline.pipeline_result import PipelineResult
from app.core.pipeline.pipeline_runner import PipelineRunner
from app.core.progress.progress_reporter import ProgressReporter
from app.core.progress.progress_stage import ProgressStage
from app.models.analysis_request import AnalysisRequest
from app.models.analysis_result import AnalysisResult
from app.models.exceptions import AnalysisError

__all__ = [
    "AnalysisService",
]


class PipelineFactory(Protocol):
    """Creates a configured analysis pipeline. Implementation stays hidden."""

    def create(self) -> Any: ...


class AnalysisService:
    """Coordinates the live analysis use case."""

    VERSION = "4.0.0"

    def __init__(self, pipeline_factory: PipelineFactory) -> None:
        self._pipeline_factory = pipeline_factory

    def analyze(
        self,
        request: AnalysisRequest,
        *,
        progress_reporter: ProgressReporter | None = None,
    ) -> AnalysisResult:
        """Run analysis for ``request`` and return the canonical outcome."""

        if not isinstance(request, AnalysisRequest):
            raise AnalysisError(
                "analyze() requires an AnalysisRequest.",
            )

        pipeline_result = self._run_pipeline(request, progress_reporter)
        return self._outcome_from_pipeline(pipeline_result)

    def analyze_with_record_id(
        self,
        request: AnalysisRequest,
        *,
        progress_reporter: ProgressReporter | None = None,
    ) -> tuple[AnalysisResult, int]:
        """Run analysis and return both its result and persisted history ID."""

        if not isinstance(request, AnalysisRequest):
            raise AnalysisError("analyze_with_record_id() requires an AnalysisRequest.")

        pipeline_result = self._run_pipeline(request, progress_reporter)
        result = self._outcome_from_pipeline(pipeline_result)
        record_id = pipeline_result.context.get(PipelineKeys.HISTORY_RECORD_ID)
        if not isinstance(record_id, int) or record_id <= 0:
            raise AnalysisError("Analysis completed without a persisted history ID.")
        return result, record_id

    def _run_pipeline(
        self,
        request: AnalysisRequest,
        progress_reporter: ProgressReporter | None,
    ) -> PipelineResult:
        context = PipelineContext(
            data={
                PipelineKeys.PDF_PATH: request.source_path,
                PipelineKeys.FILENAME: request.filename,
                PipelineKeys.ANALYSIS_TYPE: request.analysis_type,
            },
            progress_reporter=progress_reporter,
            cancellation_token=getattr(
                progress_reporter,
                "cancellation_token",
                None,
            ),
        )
        context.report_progress(
            message="Starting analysis",
            percentage=0,
            stage=ProgressStage.STARTING,
        )

        pipeline = self._pipeline_factory.create()
        pipeline_result = PipelineRunner(pipeline).run(context)

        if pipeline_result.success:
            context.report_progress(
                message="Analysis completed",
                percentage=100,
                stage=ProgressStage.COMPLETED,
            )

        return pipeline_result

    async def analyze_async(
        self,
        request: AnalysisRequest,
        *,
        progress_reporter: ProgressReporter | None = None,
    ) -> AnalysisResult:
        return self.analyze(
            request,
            progress_reporter=progress_reporter,
        )

    def result_from_pipeline(
        self,
        pipeline_result: PipelineResult,
    ) -> AnalysisResult | None:
        """Map a pipeline envelope to AnalysisResult without raising."""

        stored = pipeline_result.context.get(PipelineKeys.ANALYSIS_RESULT)
        if stored is None:
            return None
        if isinstance(stored, AnalysisResult):
            return stored
        raise TypeError("Pipeline analysis_result must be an AnalysisResult.")

    def _outcome_from_pipeline(
        self,
        pipeline_result: PipelineResult,
    ) -> AnalysisResult:
        if not pipeline_result.success:
            raise AnalysisError(
                "Research paper analysis failed.",
            ) from pipeline_result.error

        result = self.result_from_pipeline(pipeline_result)
        if result is None:
            raise AnalysisError("Analysis completed without an AnalysisResult.")
        return result

    @property
    def name(self) -> str:
        return "Research Analysis Service"

    @property
    def version(self) -> str:
        return self.VERSION
