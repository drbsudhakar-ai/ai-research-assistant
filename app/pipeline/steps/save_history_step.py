"""
===============================================================================
Project      : AI Research Assistant
Module       : Save History Pipeline Step
File         : save_history_step.py
Version      : 1.0.0

Description:
    Persists completed research analysis results.

    Responsibilities:
        - Create history record
        - Store analysis metadata
        - Save using HistoryService
        - Attach persistence result to pipeline context

===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.core.pipeline.base_pipeline_step import (
    BasePipelineStep,
)
from app.core.pipeline.pipeline_context import (
    PipelineContext,
)
from app.core.pipeline.pipeline_keys import PipelineKeys
from app.models.analysis_record import AnalysisRecord
from app.models.analysis_result import AnalysisResult
from app.models.prepared_paper import PreparedPaper
from app.services.history_service import (
    HistoryService,
)

__all__ = [
    "SaveHistoryStep",
]


class SaveHistoryStep(BasePipelineStep):
    """
    Pipeline step responsible for analysis persistence.
    """


    VERSION = "1.0.0"


    def __init__(
        self,
        history_service: HistoryService,
    ) -> None:
        """
        Initialize history saving step.

        Parameters
        ----------
        history_service:
            Service responsible for storing analysis history.
        """

        self._history_service = history_service



    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Step name.
        """

        return "Save Analysis History"



    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Save analysis result.

        Parameters
        ----------
        context:
            Shared pipeline execution context.
        """


        analysis_result = context.data.get(
            PipelineKeys.ANALYSIS_RESULT
        )


        if not isinstance(analysis_result, AnalysisResult):

            raise TypeError(
                "Canonical AnalysisResult missing from pipeline context"
            )


        paper = context.get(PipelineKeys.PREPARED_PAPER)
        paper_metadata = context.data.get(
            PipelineKeys.PAPER_METADATA,
            {},
        )

        record = self._build_record(
            analysis_result,
            paper if isinstance(paper, PreparedPaper) else None,
            paper_metadata,
        )

        record_id = self._history_service.save_analysis(record)
        # saved_record = (
        #      self._history_service.save_analysis(
        #         record
        #     )
        # )


        #
        # Store persistence result
        #

        context.data[PipelineKeys.HISTORY_RECORD_ID] = record_id
        # context.data["history_record"] = (
        #     saved_record
        # )


        self._report_progress(
            context,
            "Analysis history saved",
        )



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_record(
        self,
        analysis_result: AnalysisResult,
        paper: PreparedPaper | None,
        paper_metadata: dict[str, Any],
    ) -> AnalysisRecord:
        """
        Convert the canonical analysis outcome into a history record.
        """

        return AnalysisRecord.from_result(
            analysis_result,
            paper=paper,
            title=str(paper_metadata.get("title") or "Unknown Paper"),
            filename=str(paper_metadata.get("filename") or ""),
            input_source="PDF",
            analysis_type="Research Paper Analysis",
            total_pages=int(paper_metadata.get("pages") or 0),
            total_characters=int(paper_metadata.get("characters") or 0),
        )


    def _report_progress(
        self,
        context: PipelineContext,
        message: str,
    ) -> None:
        """
        Notify optional progress reporter.
        """

        reporter = getattr(
            context,
            "progress_reporter",
            None,
        )


        if reporter is None:
            return


        reporter.update(
            message=message,
        )